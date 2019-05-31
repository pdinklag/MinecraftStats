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
                    help='the server\'s display name (default: motd from server.properties)')
parser.add_argument('--database', '-d', type=str, required=False, default='data',
                    help='path into which to store the MinecraftStats database (default: "data")')
parser.add_argument('--skin-update-interval', type=int, required=False, default=24,
                    help='update player skins every this many hours (default 24)')
parser.add_argument('--update-inactive', required=False, action='store_true',
                    help='if set, skins of inactive players are updated as well')
parser.add_argument('--inactive-days', type=int, required=False, default=7,
                    help='number of days after which a player is considered inactive (default 7)')
parser.add_argument('--min-playtime', type=int, required=False, default=0,
                    help='number of minutes a player needs to have played before being eligible for any awards (default 0)')
parser.add_argument('--store-uncompressed', required=False, action='store_true',
                    help='if set, the database will also be stored in an uncompressed JSON form')

args = parser.parse_args()

def handle_error(e, die = False):
    print(str(e))
    if die:
        exit(1)

inactive_time = 86400 * args.inactive_days
min_playtime = args.min_playtime
skin_update_interval = 3600 * args.skin_update_interval

# paths
mcUsercacheFilename = args.server + '/usercache.json'

mcWorldDir = args.server + '/' + args.world;
mcStatsDir = mcWorldDir + '/stats'
mcAdvancementsDir = mcWorldDir + '/advancements'

# sanity checks
if not os.path.isdir(args.server):
    handle_error('not a directory: ' + args.server, True)

if not os.path.isdir(mcStatsDir):
    handle_error('no valid stat directory: ' + mcStatsDir, True)

dbFilename = args.database + '/db.json'
dbCompressedFilename = args.database + '/db.json.gz'
dbRankingsPath = args.database + '/rankings'
dbPlayerDataPath = args.database + '/playerdata'

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

# load information from previous update
if os.path.isfile(dbCompressedFilename):
    try:
        with gzip.open(dbCompressedFilename) as dbFile:
            prev_db = json.loads(dbFile.read().decode())

        players = prev_db['players']
        last_update_time = prev_db['info']['updateTime']
    except Exception as e:
        print('error loading previous database: ' + dbCompressedFilename)
        handle_error(e, True)
else:
    last_update_time = 0
    players = dict()

# read Minecraft user cache
try:
    with open(mcUsercacheFilename) as usercacheFile:
        mcUsercache = json.load(usercacheFile)
except Exception as e:
    print('failed to read Minecraft user cache: ' + args.usercache)
    handle_error(e, True)

# update player database using Minecraft user cache
# while Minecraft user cache entries can expire, the database entries do not
for mcUser in mcUsercache:
    uuid = mcUser['uuid']
    if not uuid in players:
        players[uuid] = {'name': mcUser['name']}

# update player data
hof = mcstats.Ranking()

for uuid, player in players.items():
    # cache name
    name = player['name']

    # check if data file is available
    dataFilename = mcStatsDir + '/' + uuid + '.json'
    if not os.path.isfile(dataFilename):
        # got no data for this dude
        continue

    # get last play time and determine activity
    last = int(os.path.getmtime(dataFilename))
    player['last'] = last

    inactive = ((now - last) > inactive_time)

    # update skin
    if args.update_inactive or (not inactive):
        if (not 'skin' in player) or (now - last_update_time > skin_update_interval):
            try:
                print('updating skin for ' + name + ' ...')

                profile = mojang.get_player_profile(uuid)
                try:
                    # only store suffix of url, the prefix is always the base url
                    skin = profile['textures']['SKIN']['url'][38:]
                except:
                    skin = False

                player['skin'] = skin
            except Exception as e:
                print('failed to update skin for ' + name)
                handle_error(e)

    # load data
    try:
        with open(dataFilename) as dataFile:
            data = json.load(dataFile)
    except Exception as e:
        print('failed to update player data for ' + name +
            ' (' + uuid + ')')
        handle_error(e)
        continue

    # check data version
    if 'DataVersion' in data:
        version = data['DataVersion']
    else:
        version = 0

    if version < 1451: # 17w47a is the absolute minimum
        print('unsupported data version ' + str(version) + ' for ' + name +
            ' (' + uuid + ')')
        continue

    # collapse stats
    stats = data['stats']

    # get amount of time played
    playtimeTicks = stats['minecraft:custom']['minecraft:play_one_minute'];
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
        award['best'] = {'uuid':best.id,'value':best.value}

    # add to award info list
    awards[mcstat.name] = award

# compute and write hall of fame
hof.sort()
outHallOfFame = []
for entry in hof.ranking:
    if entry.value.score[0] == 0:
        break

    outHallOfFame.append({'uuid':entry.id,'value':entry.value.score})

# write player data and construct player cache
playerCache = dict()

for uuid, player in players.items():
    # skip players with no data
    if 'last' not in player:
        continue
    playerCache[uuid] = {
        'name': player['name'],
        'last': player['last'],
    }

    if 'skin' in player:
        playerCache[uuid]['skin'] = player['skin']

    if 'stats' in player:
        with open(dbPlayerDataPath + '/' + uuid + '.json', 'w') as dataFile:
            json.dump(player['stats'], dataFile)

# copy server icon if available
if os.path.isfile(args.server + '/server-icon.png'):
    has_icon = True
    shutil.copy(args.server + '/server-icon.png', args.database)
else:
    has_icon = False

# construct update info
info = {
    'hasIcon': has_icon,
    'serverName': args.server_name,
    'updateTime': int(now),
    'inactiveDays': args.inactive_days
}

# compile database
db = {
    'info': info,
    'awards': awards,
    'players': playerCache,
    'hof': outHallOfFame
}

# write compressed database (for client)
with gzip.open(dbCompressedFilename, 'wb') as dbFile:
    dbFile.write(json.dumps(db).encode())

# write uncompressed database
if args.store_uncompressed:
    with open(dbFilename, 'w') as dbFile:
        json.dump(db, dbFile)
