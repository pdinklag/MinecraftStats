#!/usr/bin/python3
import argparse
import gzip
import json
import math
import os
import re
import shutil
import traceback

# import custom modules
import javaproperties
import mojang

from mcstats import mcstats
from mcstats.stats import *

# name->stat
statByName = dict()
for mcstat in mcstats.registry:
    statByName[mcstat.name] = mcstat

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Update Minecraft statistics')
parser.add_argument('--server', '-s', type=str, required=True,
                    help='path to the Minecraft server')
parser.add_argument('--world', '-w', type=str, required=False, default='world',
                    help='name of the server\'s main world that contains the stats directory (default "world")')
parser.add_argument('--server-name', type=str, required=False, default=None,
                    help='the server\'s display name - supports Minecraft color codes (default: motd from server.properties)')
parser.add_argument('--database', '-d', type=str, required=False, default='data',
                    help='path into which to store the MinecraftStats database (default: "data")')
parser.add_argument('--profile-update-interval', type=int, required=False, default=3,
                    help='update player skins and names every this many days (default 3)')
parser.add_argument('--update-inactive', required=False, action='store_true',
                    help='if set, skins of inactive players are updated as well')
parser.add_argument('--inactive-days', type=int, required=False, default=7,
                    help='number of days after which a player is considered inactive (default 7)')
parser.add_argument('--min-playtime', type=int, required=False, default=0,
                    help='number of minutes a player needs to have played before being eligible for any awards (default 0)')
parser.add_argument('--crown-gold', type=int, required=False, default=4,
                    help='the worth of a gold medal against the crown score (default 4)')
parser.add_argument('--crown-silver', type=int, required=False, default=2,
                    help='the worth of a silver medal against the crown score (default 2)')
parser.add_argument('--crown-bronze', type=int, required=False, default=1,
                    help='the worth of a bronze medal against the crown score (default 1)')
parser.add_argument('--players-per-page', type=int, required=False, default=100,
                    help='the number of players displayed on one page of the player list (default 100)')
parser.add_argument('--player-cache-q', type=int, required=False, default=2,
                    help='the UUID prefix length to build the playercache (default 2)')
parser.add_argument('--start-event', type=str, required=False, default=None,
                    help='starts an event with the given ID')
parser.add_argument('--event-title', type=str, required=False, default=None,
                    help='the title of the event')
parser.add_argument('--event-stat', type=str, required=False, default=None,
                    help='the stat to use for the event')
parser.add_argument('--stop-event', type=str, required=False, default=None,
                    help='stops the event with the given ID')
parser.add_argument('--delete-event', type=str, required=False, default=None,
                    help='completely deletes the event with the given ID')

args = parser.parse_args()

mcstats.CrownScore.gold = args.crown_gold
mcstats.CrownScore.silver = args.crown_silver
mcstats.CrownScore.bronze = args.crown_bronze

def handle_error(e, die = False):
    print(str(e))
    if die:
        exit(1)

inactive_time = 86400 * args.inactive_days

def is_active(last):
    global inactive_time
    return ((mcstats.now - last) <= inactive_time)

min_playtime = args.min_playtime
profile_update_interval = 86400 * args.profile_update_interval

# paths
mcWorldDir = args.server + '/' + args.world;
mcStatsDir = mcWorldDir + '/stats'
mcAdvancementsDir = mcWorldDir + '/advancements'

# sanity checks
if not os.path.isdir(args.server):
    handle_error('not a directory: ' + args.server, True)

if not os.path.isdir(mcStatsDir):
    handle_error('no valid stat directory: ' + mcStatsDir, True)

if args.start_event:
    if not args.event_title:
        handle_error('no event name given', True)

    if not args.event_stat:
        handle_error('no event stat given', True)

    if not (args.event_stat in statByName):
        handle_error('no such stat for event: ' + args.event_stat, True)

dbRankingsPath = args.database + '/rankings'
dbPlayerDataPath = args.database + '/playerdata'
dbPlayerCachePath = args.database + '/playercache'
dbEventsPath = args.database + '/events'

playerCacheQ = args.player_cache_q
playersPerPage = args.players_per_page

dbPlayersFilename = args.database + '/players.json'
dbSummaryFilename = args.database + '/summary.json.gz'

dbPlayerListPath = args.database + '/playerlist'
dbPlayerListAllFilename = dbPlayerListPath + '/all{}.json.gz'
dbPlayerListActiveFilename = dbPlayerListPath + '/active{}.json.gz'

# clean old format database
oldDbFilename = args.database + '/db.json.gz'
if os.path.isfile(oldDbFilename):
    print('Removing deprecated database file: ' + oldDbFilename)
    os.remove(oldDbFilename)

# get server.properties motd if no server name is set
if not args.server_name:
    p = re.compile('^motd=(.+)$')
    with open(args.server + '/server.properties', encoding='utf-8') as f:
        for line in f:
            m = p.match(line)
            if m:
                args.server_name = javaproperties.unescape(m.group(1))
                break

# try and load usercache
usercache = dict()
try:
    with open(args.server + '/usercache.json') as f:
        for entry in json.load(f):
            usercache[entry['uuid']] = entry['name']
except:
    print('Cannot use usercache.json for offline player lookup')

# initialize database
if not os.path.isdir(args.database):
    os.mkdir(args.database)

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
    print('failed to read player data directory: ' + args.mcStatsDir)
    handle_error(e, True)

# init events
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

# delete event
if args.delete_event:
    ename = args.delete_event
    if not ename in eventStatByName:
        handle_error('no such event to delete: ' + ename, True)

    eventStatByName.pop(ename)
    eventStats = list(filter(lambda x: x.name != ename, eventStats))

    if ename in activeEvents:
        activeEvents.discard(ename)

    os.remove(dbEventsPath + '/' + ename + '.json')
    print('deleted event: ' + ename)

# do sanity check for stop event
if args.stop_event:
    ename = args.stop_event
    if not ename in eventStatByName:
        handle_error('no such event to stop: ' + ename, True)
    elif not eventStatByName[ename].active:
        handle_error('event already stopped: ' + ename, True)

# start new event
if args.start_event:
    ename = args.start_event
    if ename in eventStatByName:
        handle_error('cannot restart existing event: ' + ename, True)

    # register
    # all sanity checks (event stat exists, etc.) have been done before
    e = mcstats.EventStat(
        ename, args.event_title, statByName[args.event_stat])

    eventStats.append(e)
    eventStatByName[ename] = e
    activeEvents.add(ename)

    print('started event: ' + args.event_title + ' (' + ename + ')')

# update player data
serverVersion = 0
hof = mcstats.Ranking()

for uuid, player in players.items():
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
    if (not 'name' in player) or active or args.update_inactive:
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
                print('failed to update profile for ' + uuid)
                print(e)
                # traceback.print_tb(e.__traceback__)

        if (not 'name' in player) and (uuid in usercache):
            # no profile available, but the UUID is in the usercache
            player['name'] = usercache[uuid]

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

# stop an event
if args.stop_event:
    # sanity checks have been done earlier
    # deactivate
    # do NOT exclude from activeEvents - we still need to save it!
    e = eventStatByName[args.stop_event]
    e.active = False
    e.stopTime = mcstats.now

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
    if ('last' in player) and ('name' in player):
        validPlayers[uuid] = player

        name = player['name']
        skin = player['skin'] if 'skin' in player else False
        last = player['last']

        serverPlayers[uuid] = {
            'name': name,
            'skin': skin,
            'last': last,
            'update': player['update']
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
if os.path.isfile(args.server + '/server-icon.png'):
    has_icon = True
    shutil.copy(args.server + '/server-icon.png', args.database)
else:
    has_icon = False

# gather info for client
info = {
    'hasIcon': has_icon,
    'serverName': args.server_name,
    'updateTime': int(mcstats.now),
    'inactiveDays': args.inactive_days,
    'minPlayTime': min_playtime,
    'crown': [args.crown_gold, args.crown_silver, args.crown_bronze],
    'cacheQ': playerCacheQ,
    'numPlayers': len(playerlist),
    'numActive': numActivePlayers,
    'playersPerPage': playersPerPage,
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
