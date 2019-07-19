#!/usr/bin/python3
import argparse
import gzip
import json
import os
import re
import shutil
import time

# get a fixed sense of "now"
now = int(time.time())

# import custom modules
import mojang

from mcstats import mcstats
from mcstats.stats import *

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

args = parser.parse_args()

def handle_error(e, die = False):
    print(str(e))
    if die:
        exit(1)

inactive_time = 86400 * args.inactive_days
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

dbRankingsPath = args.database + '/rankings'
dbPlayerDataPath = args.database + '/playerdata'
dbPlayerCachePath = args.database + '/playercache'

playerCacheQ = 2 # TODO: make parameter?

dbPlayersFilename = args.database + '/players.json'
dbSummaryFilename = args.database + '/summary.json.gz'

# get server.properties motd if no server name is set
if not args.server_name:
    p = re.compile('^motd=(.+)$')
    with open(args.server + '/server.properties') as f:
        for line in f:
            m = p.match(line)
            if m:
                args.server_name = m.group(1)
                break

# initialize database
if not os.path.isdir(args.database):
    os.mkdir(args.database)

if not os.path.isdir(dbRankingsPath):
    os.mkdir(dbRankingsPath)

if not os.path.isdir(dbPlayerDataPath):
    os.mkdir(dbPlayerDataPath)

if not os.path.isdir(dbPlayerCachePath):
    os.mkdir(dbPlayerCachePath)

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

# update player data
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

    # get last play time and determine activity
    last = int(os.path.getmtime(dataFilename))
    player['last'] = last

    inactive = ((now - last) > inactive_time)

    # update skin
    if (not 'name' in player) or args.update_inactive or (not inactive):
        if 'update' in player:
            update_time = player['update']
        else:
            update_time = 0

        if (not 'skin' in player) or (now - update_time > profile_update_interval):
            try:
                print('updating profile for ' + uuid + ' ...')
                try:
                    # try to get profile via Mojang API
                    profile = mojang.get_player_profile(uuid)

                    if not profile:
                        # unavailable, maybe the account was deleted
                        continue

                    # get name
                    player['name'] = profile['profileName']

                    # get skin
                    # only store suffix of url, the prefix is always the base url
                    skin = profile['textures']['SKIN']['url'][38:]

                except:
                    skin = False

                player['skin'] = skin

                # profile updated
                player['update'] = now

            except Exception as e:
                print('failed to update profile for ' + player['name'] + ' (' + uuid + ')')
                handle_error(e)
                continue

    # cache name
    name = player['name']

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

    # process stats
    for mcstat in mcstats.registry:
        if version >= mcstat.minVersion and version <= mcstat.maxVersion:
            value = mcstat.read(stats)
            playerStats[mcstat.name] = {'value':value}

            if not inactive:
                mcstat.enter(uuid, value)

    # init crown score
    if not inactive:
        crown = mcstats.CrownScore()
        player['crown'] = crown
        hof.enter(uuid, crown)

# compute award rankings
summaryPlayerIds = set()
awards = dict()

for mcstat in mcstats.registry:
    if not isinstance(mcstat, mcstats.Ranking):
        # this may be a legacy stat that doesn't have its own ranking
        continue

    if mcstat.name in awards:
        print('WARNING: stat name "' + mcstat.name + '" already in use')
        continue

    # sort
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

# filter valid players
validPlayers = dict()
serverPlayers = dict()

for uuid, player in players.items():
    if ('last' in player) and ('name' in player):
        validPlayers[uuid] = player
        serverPlayers[uuid] = {
            'name': player['name'],
            'skin': player['skin'],
            'last': player['last'],
            'update': player['update']
        }

        if 'stats' in player:
            with open(dbPlayerDataPath + '/' + uuid + '.json', 'w') as dataFile:
                json.dump(player['stats'], dataFile)

players = validPlayers

# write players for next server update
with open(dbPlayersFilename, 'w') as playersFile:
    json.dump(serverPlayers, playersFile)

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
    'updateTime': int(now),
    'inactiveDays': args.inactive_days,
    'cacheQ': playerCacheQ
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
    }

# write summary for client
summary = {
    'info': info,
    'players': summaryPlayers,
    'awards': awards,
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
    })

for key, cache in playercache.items():
    with open(dbPlayerCachePath + '/' + key + '.json', 'w') as cacheFile:
        json.dump(cache, cacheFile)
