#!/usr/bin/python3
import argparse
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

args = parser.parse_args()

inactive_time = 86400 * args.inactive_days
skin_update_interval = 3600 * args.skin_update_interval

# paths
mcUsercacheFilename = args.server + '/usercache.json'
mcStatsDir = args.server + '/' + args.world + '/stats'

# sanity checks
if not os.path.isdir(args.server):
    print('not a directory: ' + args.server)
    exit(1)

if not os.path.isdir(mcStatsDir):
    print('no valid stat directory: ' + mcStatsDir)
    exit(1)

dbInfoFilename = args.database + '/info.json'
dbPlayersFilename = args.database + '/players.json'
dbAwardsFilename = args.database + '/awards.json'
dbHofFilename = args.database + '/hof.json'
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

# load information about last update
last_update_time = 0
if os.path.isfile(dbInfoFilename):
    try:
        with open(dbInfoFilename) as dbInfoFile:
            last_info = json.load(dbInfoFile)

        last_update_time = last_info['updateTime']
        print('last update was at: ' + str(last_update_time))
    except:
        print('error loading info file: ' + dbInfoFilename)

# load player cache
if os.path.isfile(dbPlayersFilename):
    try:
        with open(dbPlayersFilename) as dbPlayersFile:
            players = json.load(dbPlayersFile)
    except:
        print('error loading players file: ' + dbPlayersFilename)
        exit(1)
else:
    players = dict()

# read Minecraft user cache
try:
    with open(mcUsercacheFilename) as usercacheFile:
        mcUsercache = json.load(usercacheFile)
except:
    print('failed to read Minecraft user cache: ' + args.usercache)
    exit(1)

# update player database using Minecraft user cache
# while Minecraft user cache entries can expire, the database entries do not
for mcUser in mcUsercache:
    uuid = mcUser['uuid']
    if not uuid in players:
        players[uuid] = {'name': mcUser['name']}

# update player data
hof = mcstats.CrownScoreRanking()

for uuid, player in players.items():
    # cache name
    name = player['name']

    # check if data file is available
    dataFilename = mcStatsDir + '/' + uuid + '.json'
    if not os.path.isfile(dataFilename):
        print('no player data available for ' + name +
            '(' + uuid + ')')
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
            except:
                print('failed to update skin for ' + name)

    # load data
    try:
        with open(dataFilename) as dataFile:
            data = json.load(dataFile)
    except:
        print('failed to update player data for ' + name +
            '(' + uuid + ')')
        continue

    # check data version
    if 'DataVersion' in data:
        version = data['DataVersion']
    else:
        version = 0

    if version < 1452:
        print('unsupported data version ' + str(version) + ' for ' + name +
            '(' + uuid + ')')
        continue

    # init database data
    playerStats = dict()
    player['stats'] = playerStats

    # process stats
    stats = data['stats']
    for mcstat in mcstats.registry:
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
    if mcstat.name in awards:
        print('WARNING: stat name "' + mcstat.name + '" already in use')
        continue

    # sort
    mcstat.sort()

    # process crown score points
    for i in range(0, len(mcstat.ranking)):
        (id, ranking) = mcstat.ranking[i]
        player = players[id]
        player['stats'][mcstat.name]['rank'] = i+1

        if i < 3:
            player['crown'].increase(i)

    # write ranking
    outRanking = []
    for (id, value) in mcstat.ranking:
        outRanking.append({'uuid':id,'value':value})

    with open(dbRankingsPath + '/' + mcstat.name + '.json', 'w') as rankingFile:
        json.dump(outRanking, rankingFile)

    # set first rank in award info
    award = mcstat.meta
    if(len(mcstat.ranking) > 0):
        (id, value) = mcstat.ranking[0]
        award['best'] = {'uuid':id,'value':value}

    # add to award info list
    awards[mcstat.name] = award

# write award info
with open(dbAwardsFilename, 'w') as awardsFile:
    json.dump(awards, awardsFile)

# compute and write hall of fame
hof.sort()
outHallOfFame = []
for (id, crown) in hof.ranking:
    if crown.score[0] == 0:
        break

    outHallOfFame.append({'uuid':id,'value':crown.score})

with open(dbHofFilename, 'w') as hofFile:
    json.dump(outHallOfFame, hofFile)

# write player data
playerCache = dict()

for uuid, player in players.items():
    playerCache[uuid] = {
        'name': player['name'],
        'last': player['last'],
    }

    if 'skin' in player:
        playerCache[uuid]['skin'] = player['skin']

    if 'stats' in player:
        with open(dbPlayerDataPath + '/' + uuid + '.json', 'w') as dataFile:
            json.dump(player['stats'], dataFile)

# write player cache
with open(dbPlayersFilename, 'w') as dbPlayersFile:
    json.dump(playerCache, dbPlayersFile)

# copy server icon if available
if os.path.isfile(args.server + '/server-icon.png'):
    has_icon = True
    shutil.copy(args.server + '/server-icon.png', args.database)
else:
    has_icon = False

# write info file
info = {
    'hasIcon': has_icon,
    'serverName': args.server_name,
    'updateTime': int(now),
    'inactiveDays': args.inactive_days
}

with open(dbInfoFilename, 'w') as dbInfoFile:
    json.dump(info, dbInfoFile)
