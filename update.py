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

# ensure config
if not config.server.path:
    handle_error('server.path not configured, please edit ' + args.config, True)

mcstats.CrownScore.gold = config.crown.gold
mcstats.CrownScore.silver = config.crown.silver
mcstats.CrownScore.bronze = config.crown.bronze

inactive_time = 86400 * config.players.inactiveDays

def is_active(last):
    global inactive_time
    return ((mcstats.now - last) <= inactive_time)

min_playtime = config.players.minPlaytime
profile_update_interval = 86400 * config.players.profileUpdateInterval

# paths
serverPath = config.server.path
mcWorldDir = serverPath + '/' + config.server.worldName;
mcStatsDir = mcWorldDir + '/stats'
mcAdvancementsDir = mcWorldDir + '/advancements'

# sanity checks
if not os.path.isdir(serverPath):
    handle_error('not a directory: ' + serverPath, True)

if not os.path.isdir(mcStatsDir):
    handle_error('no valid stat directory: ' + mcStatsDir, True)

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
dbRankingsPath = config.database + '/rankings'
dbPlayerDataPath = config.database + '/playerdata'
dbPlayerCachePath = config.database + '/playercache'
dbEventsPath = config.database + '/events'

playerCacheQ = config.client.playerCacheUUIDPrefix
playersPerPage = config.client.playersPerPage

dbPlayersFilename = config.database + '/players.json'
dbSummaryFilename = config.database + '/summary.json.gz'

dbPlayerListPath = config.database + '/playerlist'
dbPlayerListAllFilename = dbPlayerListPath + '/all{}.json.gz'
dbPlayerListActiveFilename = dbPlayerListPath + '/active{}.json.gz'

# clean old format database
oldDbFilename = config.database + '/db.json.gz'
if os.path.isfile(oldDbFilename):
    print('Removing deprecated database file: ' + oldDbFilename)
    os.remove(oldDbFilename)

# get server.properties motd if no server name is set
if config.server.customName:
    serverName = config.server.customName
else:
    p = re.compile('^motd=(.+)$')
    with open(serverPath + '/server.properties', encoding='utf-8') as f:
        for line in f:
            m = p.match(line)
            if m:
                serverName = javaproperties.unescape(m.group(1)).replace('\n', '<br>')
                break

# try and load usercache
usercache = dict()
try:
    with open(serverPath + '/usercache.json') as f:
        for entry in json.load(f):
            usercache[entry['uuid']] = entry['name']
except:
    handle_error('Cannot use usercache.json for offline player lookup')

# exclude players
excludePlayers = set()

for uuid in config.players.excludeUUIDs:
    excludePlayers.add(uuid)

# exclude banned players
if config.players.excludeBanned:
    try:
        with open(serverPath + '/banned-players.json') as f:
            for entry in json.load(f):
                excludePlayers.add(entry['uuid'])
    except:
        handle_error('Cannot use banned-players.json for banned player exclusion')

# exclude ops
if config.players.excludeOps:
    try:
        with open(serverPath + '/ops.json') as f:
            for entry in json.load(f):
                excludePlayers.add(entry['uuid'])
    except:
        handle_error('Cannot use ops.json for op exclusion')

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

# find available player IDs in stats dir
try:
    for file in os.listdir(mcStatsDir):
        if file.endswith('.json'):
            uuid = file[:-5] # cut off '.json' extension
            if not uuid in players:
                players[uuid] = {}
except Exception as e:
    print('failed to read player data directory: ' + mcStatsDir)
    handle_error(e, True)

# init event stats
eventStats = []
eventStatByName = dict()
activeEvents = set()

try:
    for file in os.listdir(dbEventsPath):
        if file.endswith('.json'):
            with open(dbEventsPath + '/' + file) as eventDataFile:
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
    # check if uuid is excluded
    if uuid in excludePlayers:
        continue

    # check if data file is available
    dataFilename = mcStatsDir + '/' + uuid + '.json'
    if not os.path.isfile(dataFilename):
        # got no data for this dude
        continue

    # load data
    try:
        with open(dataFilename) as dataFile:
            data = json.load(dataFile)
    except Exception as e:
        print('failed to update player data for ' + uuid)
        handle_error(e)
        continue

    # check data version
    if 'DataVersion' in data:
        version = data['DataVersion']
    else:
        version = 0

    if version < 1451: # 17w47a is the absolute minimum
        print('unsupported data version ' + str(version) + ' for ' + uuid)
        continue

    serverVersion = max(serverVersion, version)

    # collapse stats
    stats = data['stats']

    # get amount of time played
    playtimeTicks = 0
    if 'minecraft:custom' in stats:
        custom = stats['minecraft:custom']
        if 'minecraft:play_one_minute' in custom:
            playtimeTicks = custom['minecraft:play_one_minute']

    playtimeMinutes = playtimeTicks / (20 * 60);
    if playtimeMinutes < min_playtime:
        # invalidate player and continue
        player.pop('name', None)
        player.pop('last', None)
        continue

    # get last play time and determine activity
    last = int(os.path.getmtime(dataFilename))
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

    # try and load advancements into stats
    advFilename = mcAdvancementsDir + '/' + uuid + '.json'
    try:
        with open(advFilename) as advFile:
            stats['advancements'] = json.load(advFile)
    except:
        stats['advancements'] = dict()

    # process registry and event stats
    for mcstat in mcstats.registry + eventStats:
        if mcstat.isEligible(version):
            value = mcstat.read(stats)

            if mcstat.playerStatRelevant:
                playerStats[mcstat.name] = {'value':value}

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

    with open(dbRankingsPath + '/' + mcstat.name + '.json', 'w') as rankingFile:
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
    if (not uuid in excludePlayers) and  ('last' in player) and ('name' in player) and ('stats' in player):
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

        with open(dbPlayerDataPath + '/' + uuid + '.json', 'w') as dataFile:
            json.dump(player['stats'], dataFile)

players = validPlayers

# write players for next server update
with open(dbPlayersFilename, 'w') as playersFile:
    json.dump(serverPlayers, playersFile)

# write event data
for ename in activeEvents:
    with open(dbEventsPath + '/' + ename + '.json', 'w') as dataFile:
        json.dump(eventStatByName[ename].serialize(), dataFile)

# copy server icon if available
if os.path.isfile(serverPath + '/server-icon.png'):
    has_icon = True
    shutil.copy(serverPath + '/server-icon.png', config.database)
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
    with open(dbPlayerCachePath + '/' + key + '.json', 'w') as cacheFile:
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
