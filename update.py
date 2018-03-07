#!/usr/bin/python3

import argparse
import json
import os
import time

from collections import namedtuple

# import statistics modules
from mcstats import __mcstats__
from mcstats import *

# Crown score (a meta statistic)
class CrownScore:
    def __init__(self):
        self.score = [0,0,0,0]

    def increase(self, i):
        self.score[i+1] += 1
        self.score[0] = 4*self.score[1] + 2*self.score[2] + self.score[3]

class CrownScoreRanking(__mcstats__.Ranking):
    def sort(self):
        self.ranking = sorted(
            self.ranking, key = lambda x : x[1].score[0], reverse = True)

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Update Minecraft statistics')
parser.add_argument('--stats', '-s', type=str, required=True,
                    help='path to the stats directory of the Minecraft world')
parser.add_argument('--usercache', '-u', type=str, required=True,
                    help='path to Minecraft server\'s usercache.json')
parser.add_argument('--database', '-d', type=str, required=False, default='data',
                    help='path into which to store the MinecraftStats database')
parser.add_argument('--inactive-days', type=int, required=False, default=7,
                    help='number of days after which a player is considered inactive')

args = parser.parse_args()

# sanity checks
if not os.path.isdir(args.stats):
    print('not a directory: ' + args.stats)
    exit(1)

# paths
dbPlayersFilename = args.database + '/players.json'
dbAwardsFilename = args.database + '/awards.json'
dbHofFilename = args.database + '/hof.json'
dbRankingsPath = args.database + '/rankings'
dbPlayerDataPath = args.database + '/playerdata'

# initialize database
if not os.path.isdir(args.database):
    os.mkdir(args.database);

if not os.path.isdir(dbRankingsPath):
    os.mkdir(dbRankingsPath);

if not os.path.isdir(dbPlayerDataPath):
    os.mkdir(dbPlayerDataPath);

# load player cache
try:
    with open(dbPlayersFilename) as dbPlayersFile:
        players = json.load(dbPlayersFile)
except:
    players = dict()

# read Minecraft user cache
try:
    with open(args.usercache) as usercacheFile:
        mcUsercache = json.load(usercacheFile)
except:
    print('failed to read Minecraft user cache: ' + args.usercache)
    exit(1)

# update player database using Minecraft user cache
# while Minecraft user cache entries can expire, the database entries do not
for mcUser in mcUsercache:
    players[mcUser['uuid']] = {'name': mcUser['name']}

# update player data
hof = CrownScoreRanking()

for uuid, player in players.items():
    # cache name
    name = player['name']

    # check if data file is available
    dataFilename = args.stats + '/' + uuid + '.json'
    if not os.path.isfile(dataFilename):
        print('no player data available for ' + name +
            '(' + uuid + ')')
        continue

    # get last play time and determine activity
    last = int(os.path.getmtime(dataFilename))
    inactive = ((time.time() - last) > 86400 * args.inactive_days)

    player['last'] = last
    player['inactive'] = inactive

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

    stats = data['stats']

    # init database data
    playerStats = dict()
    player['stats'] = playerStats

    # process stats
    for mcstat in __mcstats__.registry:
        value = mcstat.read(stats)
        playerStats[mcstat.name] = {'value':value}

        if not inactive:
            mcstat.enter(uuid, value)

    # init crown score
    if not inactive:
        crown = CrownScore()
        player['crown'] = crown
        hof.enter(uuid, crown)

# compute award rankings
awards = dict()

for mcstat in __mcstats__.registry:
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
        'inactive': player['inactive']
    }

    if 'stats' in player:
        with open(dbPlayerDataPath + '/' + uuid + '.json', 'w') as dataFile:
            json.dump(player['stats'], dataFile)

# write player cache
with open(dbPlayersFilename, 'w') as dbPlayersFile:
    json.dump(playerCache, dbPlayersFile)
