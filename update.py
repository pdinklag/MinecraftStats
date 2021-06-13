#!/usr/bin/env python3
import argparse
import collections
import datetime 
import gzip
import json
import math
import os
import re
import shutil
import sys
import traceback
import types

# import custom modules
import javaproperties
import mojang

from mcstats import config
from mcstats import mcstats
from mcstats.util import handle_error
from mcstats.util import RecursiveNamespace
from mcstats.util import merge_dict
from mcstats.stats import *

# default config
configJson = config.defaultConfig

# name->stat
statByName = dict()
for mcstat in mcstats.registry:
    statByName[mcstat.name] = mcstat

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Update MinecraftStats')
parser.add_argument('config', type=str, help='the configuration to use')

args = parser.parse_args()

# load config
if os.path.isfile(args.config):
    with open(args.config, 'r', encoding="utf8") as configFile:
        merge_dict(configJson, json.load(configFile))
else:
    # save default
    print('writing default config to ' + args.config)
    with open(args.config, 'w') as configFile:
        json.dump(configJson, configFile, indent=4)

config = RecursiveNamespace(**configJson)

# get sources
sources = []
if hasattr(config.server, 'path') and config.server.path:
    handle_error('server.path is deprecated, please use server.sources instead to configure your paths')
    
    worldName = config.server.worldName
    if isinstance(config.server.path, list):
        serverPaths = config.server.path
    else:
        serverPaths = [config.server.path]

    for path in serverPaths:
        sources.append((path, worldName))

if isinstance(config.server.sources, list):
    for e in config.server.sources:
        sources.append((e.path, e.worldName))

if len(sources) == 0:
    handle_error('server.sources not configured, please consult the documentation and edit ' + args.config, True)

statsDirs = []
advancementDirs = []

for (path, worldName) in sources:
    if not os.path.isdir(path):
        handle_error('invalid path in server.sources: ' + str(path), True)

    worldDir = os.path.join(path, worldName)
    statsDirs.append(os.path.join(worldDir, 'stats'))
    advancementDirs.append(os.path.join(worldDir, 'advancements'))

primaryServerPath = sources[0][0]

mcstats.CrownScore.gold = config.crown.gold
mcstats.CrownScore.silver = config.crown.silver
mcstats.CrownScore.bronze = config.crown.bronze

inactive_time = 86400 * config.players.inactiveDays

def is_active(last):
    global inactive_time
    return ((mcstats.now - last) <= inactive_time)

min_playtime = config.players.minPlaytime
profile_update_interval = 86400 * config.players.profileUpdateInterval

# initialize event definitions
Event = collections.namedtuple('Event', ['name', 'title', 'stat', 'startTime', 'endTime'])
eventTimeFormat = '%Y-%m-%d %H:%M'

events = []
for e in config.events:
    if not e.stat in statByName:
        handle_error('ERROR: event ' + e.name + ' refers to unknown stat "' + e.stat + '"')
        continue

    stat = statByName[e.stat]
    startTime = int(datetime.datetime.strptime(e.startTime, eventTimeFormat).timestamp())
    endTime = int(datetime.datetime.strptime(e.endTime, eventTimeFormat).timestamp())
    
    if startTime >= endTime:
        handle_error('ERROR: event ' + e.name + ': end time (' + e.endTime + ' lies before start time (' + e.startTime + ')')
        continue
    
    events.append(Event(title=e.title, name=e.name, stat=stat, startTime=startTime, endTime=endTime))

# init paths
dbRankingsPath = os.path.join(config.database, 'rankings')
dbPlayerDataPath = os.path.join(config.database, 'playerdata')
dbPlayerCachePath = os.path.join(config.database, 'playercache')
dbEventsPath = os.path.join(config.database, 'events')

playerCacheQ = config.client.playerCacheUUIDPrefix
playersPerPage = config.client.playersPerPage

dbPlayersFilename = os.path.join(config.database, 'players.json')
dbSummaryFilename = os.path.join(config.database, 'summary.json.gz')

dbPlayerListPath = os.path.join(config.database, 'playerlist')
dbPlayerListAllFilename = os.path.join(dbPlayerListPath, 'all{}.json.gz')
dbPlayerListActiveFilename = os.path.join(dbPlayerListPath, 'active{}.json.gz')

# get server.properties motd if no server name is set
if config.server.customName:
    serverName = config.server.customName
else:
    p = re.compile('^motd=(.+)$')
    with open(os.path.join(primaryServerPath, 'server.properties'), encoding='utf-8') as f:
        for line in f:
            m = p.match(line)
            if m:
                serverName = javaproperties.unescape(m.group(1)).replace('\n', '<br>')
                break

# try and load usercache
usercache = dict()
for (path, _) in sources:
    usercacheFile = os.path.join(path, 'usercache.json')
    try:
        with open(usercacheFile) as f:
            for entry in json.load(f):
                usercache[entry['uuid']] = entry['name']
    except:
        handle_error('Cannot open ' + usercacheFile + ' for offline player lookup')

# exclude players
excludePlayers = set()

for uuid in config.players.excludeUUIDs:
    excludePlayers.add(uuid)

# exclude banned players
if config.players.excludeBanned:
    for (path, _) in sources:
        bannedPlayersFile = os.path.join(path, 'banned-players.json')
        try:
            with open(bannedPlayersFile) as f:
                for entry in json.load(f):
                    excludePlayers.add(entry['uuid'])
        except:
            handle_error('Cannot open ' + bannedPlayersFile + ' for banned player exclusion')

# exclude ops
if config.players.excludeOps:
    for (path, _) in sources:
        opsFile = os.path.join(path, 'ops.json')
        try:
            with open(opsFile) as f:
                for entry in json.load(f):
                    excludePlayers.add(entry['uuid'])
        except:
            handle_error('Cannot open ' + opsFile + ' for op exclusion')

# initialize database
if not os.path.isdir(config.database):
    os.mkdir(config.database)

if not os.path.isdir(dbRankingsPath):
    os.mkdir(dbRankingsPath)

if not os.path.isdir(dbEventsPath):
    os.mkdir(dbEventsPath)

if not os.path.isdir(dbPlayerDataPath):
    os.mkdir(dbPlayerDataPath)

if not os.path.isdir(dbPlayerCachePath):
    os.mkdir(dbPlayerCachePath)

if not os.path.isdir(dbPlayerListPath):
    os.mkdir(dbPlayerListPath)

# load information from previous update
if os.path.isfile(dbPlayersFilename):
    try:
        with open(dbPlayersFilename) as playersFile:
            players = json.load(playersFile)
    except Exception as e:
        print('error loading previous database: ' + dbPlayersFilename)
        handle_error(e, True)
else:
    players = dict()

# remove excluded players
for uuid in excludePlayers:
    if uuid in players:
        del players[uuid]

# find available player IDs in stats dirs
for statsDir in statsDirs:
    try:
        for file in os.listdir(statsDir):
            if file.endswith('.json'):
                uuid = file[:-5] # cut off '.json' extension
                if (not uuid in players) and (not uuid in excludePlayers):
                    players[uuid] = {}
    except Exception as e:
        print('failed to read player data directory: ' + statsDir)
        handle_error(e, True)

# init event stats
eventStats = []
eventStatByName = dict()
activeEvents = set()

try:
    for file in os.listdir(dbEventsPath):
        if file.endswith('.json'):
            with open(os.path.join(dbEventsPath, file)) as eventDataFile:
                e = mcstats.EventStat.deserialize(
                    json.load(eventDataFile), statByName)

                eventStats.append(e)
                eventStatByName[e.name] = e

                if e.active:
                    e.ranking = [] # clear, will be re-calculated
                    activeEvents.add(e.name)

except Exception as e:
    print('failed to read event data directory: ' + dbEventsPath)
    handle_error(e, True)

# possibly start events
for e in events:
    if mcstats.now >= e.startTime and mcstats.now < e.endTime:
        # this event should be running
        if not e.name in activeEvents:
            if e.name in eventStatByName:
                handle_error('ERROR: duplicate event ' + e.name)
                continue
        
            # ... but it's not - start it
            eventStat = mcstats.EventStat(e.name, e.title, e.stat)
            eventStats.append(eventStat)
            eventStatByName[e.name] = eventStat
            activeEvents.add(e.name)
            print('event "' + e.title + '" (' + e.name + ') has started!')

# update player data
serverVersion = 0
hof = mcstats.Ranking()

for uuid, player in players.items():
    # check if any data files are available and get basic data
    last = 0
    playtimeTicks = 0
    version = 0
    datasets = []
    
    for i, statsDir in enumerate(statsDirs):
        dataFilename = os.path.join(statsDir, uuid + '.json')
        if os.path.isfile(dataFilename):
            last = max(last, int(os.path.getmtime(dataFilename)))
            
            with open(dataFilename) as f:
                data = json.load(f)

            if 'DataVersion' in data:
                version = max(version, data['DataVersion'])

            if 'stats' in data:
                stats = data['stats']
                
                if 'minecraft:custom' in stats:
                    custom = stats['minecraft:custom']
                    if 'minecraft:play_time' in custom:
                        playtimeTicks += int(custom['minecraft:play_time']) # new in 21w16a (data version 2711)
                    if 'minecraft:play_one_minute' in custom:
                        playtimeTicks += int(custom['minecraft:play_one_minute'])

                # also attempt to load advancements
                advFilename = os.path.join(advancementDirs[i], uuid + '.json')
                if os.path.isfile(advFilename):
                    with open(advFilename) as advFile:
                        stats['advancements'] = json.load(advFile)

                datasets.append(stats)
    
    # check if any data is available
    if len(datasets) == 0:
        continue
    
    # check data version
    if 'DataVersion' in data:
        version = data['DataVersion']
    else:
        version = 0

    if version < 1451: # 17w47a is the absolute minimum
        print('unsupported data version ' + str(version) + ' for ' + uuid)
        continue

    # find latest overall server version
    serverVersion = max(serverVersion, version)

    # get total amount of time played
    playtimeMinutes = playtimeTicks / (20 * 60);
    if playtimeMinutes < min_playtime:
        # invalidate player and continue
        player.pop('name', None)
        player.pop('last', None)
        continue

    # determine activity
    player['last'] = last
    active = is_active(last)
    
    # update skin
    if (not 'name' in player) or active or config.players.updateInactive:
        if 'update' in player:
            update_time = player['update']
        else:
            update_time = 0

        if (not 'name' in player) or (not 'skin' in player) or (mcstats.now - update_time > profile_update_interval):
            try:
                print('updating profile for ' + uuid + ' ...')

                # try to get profile via Mojang API
                profile = mojang.get_player_profile(uuid)
                
                if profile:
                    # get name and skin
                    player['name'] = profile['name']
                    player['skin'] = profile['skin']

                # profile updated
                player['update'] = mcstats.now

            except KeyboardInterrupt as e:
                handle_error('cancelled', True)

            except Exception as e:
                print('\tfailed to update profile for ' + uuid)
                print(e)
                # traceback.print_tb(e.__traceback__)

        if (not 'name' in player) and (uuid in usercache):
            # no profile available, but the UUID is in the usercache
            player['name'] = usercache[uuid]

        if (not 'name' in player):
            # there is no way to find the name of this player
            # this may happen if the player has no valid Mojang UUID
            # since the ID also no longer appears in the usercache, chances are we're dealing with an inactive player anyway
            print('\texcluding invalid player ' + uuid)
            continue

    # init database data
    playerStats = dict()
    player['stats'] = playerStats

    # process registry and event stats for each dataset
    for stats in datasets:
        for mcstat in mcstats.registry + eventStats:
            if mcstat.isEligible(version):
                value = mcstat.read(stats)
                if mcstat.playerStatRelevant:
                    if mcstat.name in playerStats:
                        value = mcstat.aggregate(playerStats[mcstat.name], value)
                    
                    playerStats[mcstat.name] = value

    # enter into rankings
    for mcstat in mcstats.registry + eventStats:
        if mcstat.name in playerStats:
            value = playerStats[mcstat.name]['value']
            playerStats[mcstat.name] = {'value': value} # collapse
            
            if mcstat.canEnterRanking(uuid, active):
                mcstat.enter(uuid, value)

    # init crown score
    if active:
        crown = mcstats.CrownScore()
        player['crown'] = crown
        hof.enter(uuid, crown)

# compute award rankings
summaryPlayerIds = set()
awards = dict()

for mcstat in mcstats.registry:
    if mcstat.linkedStat:
        continue

    if serverVersion > mcstat.maxVersion:
        # no longer supported, but don't print a warning
        continue

    if serverVersion < mcstat.minVersion:
        print('stat "' + mcstat.name + '" is not supported by server version '
              + str(serverVersion) + ' (required: ' + str(mcstat.minVersion) + ')')
        continue

    if mcstat.name in awards:
        print('WARNING: stat name "' + mcstat.name + '" already in use')
        continue

    # sort ranking
    mcstat.sort()

    # process crown score points
    for i in range(0, len(mcstat.ranking)):
        entry = mcstat.ranking[i]
        player = players[entry.id]
        player['stats'][mcstat.name]['rank'] = i+1

        if i < 3:
            player['crown'].increase(i)

    # write ranking
    outRanking = []
    for entry in mcstat.ranking:
        outRanking.append({'uuid':entry.id,'value':entry.value})

    with open(os.path.join(dbRankingsPath, mcstat.name + '.json'), 'w') as rankingFile:
        json.dump(outRanking, rankingFile)

    # set first rank in award info
    award = mcstat.meta
    if(len(mcstat.ranking) > 0):
        best = mcstat.ranking[0]
        award['best'] = {'uuid': best.id, 'value': best.value}
        summaryPlayerIds.add(best.id)

    # add to award info list
    awards[mcstat.name] = award

# possibly stop events
for e in events:
    if mcstats.now >= e.endTime and e.name in activeEvents:
        # stop event
        eventStat = eventStatByName[e.name]
        eventStat.active = False
        eventStat.stopTime = mcstats.now
        # nb: do NOT exclude from activeEvents - we still need to save it!
        print('event "' + e.title + '" (' + e.name + ') has ended!')

# process events
summaryEvents = dict()

for event in eventStats:
    # check version
    if serverVersion < mcstat.minVersion:
        print('event "' + event.name + '" is not supported by server version '
              + str(serverVersion) + ' (required: ' + str(event.minVersion) + ')')
        continue

    # sort ranking
    event.sort()

    # create summary
    esummary = {
        'title':     event.title,
        'link':      event.link.name,
        'startTime': event.startTime,
        'stopTime':  event.stopTime,
        'active':    event.active,
    }

    if(len(event.ranking) > 0):
        best = event.ranking[0]
        esummary['best'] = {'uuid': best.id, 'value': best.value}
        summaryPlayerIds.add(best.id)

    summaryEvents[event.name] = esummary

# filter valid players
validPlayers = dict()
serverPlayers = dict()

playerlist = []
numActivePlayers = 0

for uuid, player in players.items():
    if ('last' in player) and ('name' in player) and ('stats' in player):
        validPlayers[uuid] = player

        name = player['name']
        skin = player['skin'] if 'skin' in player else False
        last = player['last']

        serverPlayers[uuid] = {
            'name': name,
            'skin': skin,
            'last': last,
            'update': player['update'] if 'update' in player else 0
        }

        clientInfo = {
            'uuid': uuid,
            'name': name,
            'skin': skin,
            'last': last,
        }

        playerlist.append(clientInfo)

        if is_active(last):
            numActivePlayers += 1

        with open(os.path.join(dbPlayerDataPath, uuid + '.json'), 'w') as dataFile:
            json.dump(player['stats'], dataFile)

players = validPlayers

# write players for next server update
with open(dbPlayersFilename, 'w') as playersFile:
    json.dump(serverPlayers, playersFile)

# write event data
for ename in activeEvents:
    with open(os.path.join(dbEventsPath , ename + '.json'), 'w') as dataFile:
        json.dump(eventStatByName[ename].serialize(), dataFile)

# copy server icon if available
serverIconFile = os.path.join(primaryServerPath, 'server-icon.png')
if os.path.isfile(serverIconFile):
    has_icon = True
    shutil.copy(serverIconFile, config.database)
else:
    has_icon = False

# gather info for client
info = {
    'hasIcon': has_icon,
    'serverName': serverName,
    'updateTime': int(mcstats.now),
    'inactiveDays': config.players.inactiveDays,
    'minPlayTime': min_playtime,
    'crown': [config.crown.gold, config.crown.silver, config.crown.bronze],
    'cacheQ': playerCacheQ,
    'numPlayers': len(playerlist),
    'numActive': numActivePlayers,
    'playersPerPage': playersPerPage,
    'showLastOnline': config.client.showLastOnline,
}

# write hall of fame for client
# compute hall of fame
hof.sort()
outHof = []
for entry in hof.ranking:
    if entry.value.score[0] == 0:
        break

    outHof.append({
        'uuid': entry.id,
        'value': entry.value.score
    })
    summaryPlayerIds.add(entry.id)

# summary players
summaryPlayers = dict()
for uuid in summaryPlayerIds:
    player = players[uuid]
    summaryPlayers[uuid] = {
        'name': player['name'],
        'skin': player['skin'] if ('skin' in player) else False,
        'last': player['last'],
    }

# TODO: summarize events (id, display name, current best)

# write summary for client
summary = {
    'info': info,
    'players': summaryPlayers,
    'awards': awards,
    'events': summaryEvents,
    'hof': outHof,
}

with gzip.open(dbSummaryFilename, 'wb') as summaryFile:
    summaryFile.write(json.dumps(summary).encode())

# create player cache for client
playercache = dict()
for uuid, player in players.items():
    key = uuid[:playerCacheQ]
    if not key in playercache:
        playercache[key] = list()

    playercache[key].append({
        'uuid': uuid,
        'name': player['name'],
        'skin': player['skin'] if ('skin' in player) else False,
        'last': player['last']
    })

for key, cache in playercache.items():
    with open(os.path.join(dbPlayerCachePath, key + '.json'), 'w') as cacheFile:
        json.dump(cache, cacheFile)

# write player list (all players)
playerlist = sorted(playerlist, key=lambda x: x['name'].lower())
for i in range(0, len(playerlist), playersPerPage):
    page = int(i / playersPerPage)
    with gzip.open(dbPlayerListAllFilename.format(page + 1), 'wb') as f:
        f.write(json.dumps(
            playerlist[i : i + playersPerPage]).encode())

# write active player list
playerlist = list(filter(lambda x: is_active(x['last']), playerlist))
for i in range(0, len(playerlist), playersPerPage):
    page = int(i / playersPerPage)
    with gzip.open(dbPlayerListActiveFilename.format(page + 1), 'wb') as f:
        f.write(json.dumps(
            playerlist[i : i + playersPerPage]).encode())

# done
print('update finished')
