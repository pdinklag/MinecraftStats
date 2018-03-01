#!/usr/bin/python3

import argparse
import json
import os

from collections import namedtuple

# import statistics modules
from mcstats import __mcstats__
from mcstats import *

# Crown score (a meta statistic)
def initCrownScore():
    return [0,0,0,0]

def increaseCrownScore(score, i):
    score[i+1] += 1
    score[0] = 4*score[1] + 2*score[2] + score[3]

class CrownScoreRanking(__mcstats__.Ranking):
    def sort(self):
        self.ranking = sorted(
            self.ranking, key = lambda x : x[1][0], reverse = True)

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Update Minecraft statistics')
parser.add_argument('--stats', '-s', type=str, required=True,
                    help='the path to the stats directory of the Minecraft world')
parser.add_argument('--database', '-d', type=str, required=True,
                    help='the path into which to store the MinecraftStats database')

args = parser.parse_args()

# sanity checks
if not os.path.isdir(args.stats):
    print('not a directory: ' + args.stats)
    exit(1)

# paths
mcUsercacheFilename = args.stats + '/usercache.json'

dbPlayersFilename = args.database + '/players.json'
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
    with open(mcUsercacheFilename) as mcUsercacheFile:
        mcUsercache = json.load(mcUsercacheFile)
except:
    print('failed to read Minecraft user cache: ' + mcUsercacheFilename)
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

    # get last play time
    last = int(os.path.getmtime(dataFilename))
    player['last'] = last

    # TODO: determine if player is eligible for awards

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
    playerData = dict()
    playerData['uuid'] = uuid
    playerData['name'] = name
    playerData['last'] = last
    playerStats = dict()

    # process stats
    for mcstat in __mcstats__.registry:
        value = mcstat.read(stats)
        mcstat.enter(uuid, value)
        playerStats[mcstat.name] = {'value':value}

    playerData['stats'] = playerStats
    player['data'] = playerData

    # init crown score
    crown = initCrownScore()
    player['crown'] = crown
    hof.enter(uuid, crown)

# compute award rankings
for mcstat in __mcstats__.registry:
    # sort
    mcstat.sort()

    # process crown score points
    for i in range(0, len(mcstat.ranking)):
        (id, ranking) = mcstat.ranking[i]
        player = players[id]
        player['data']['stats'][mcstat.name]['rank'] = i+1

        if i < 3:
            increaseCrownScore(player['crown'], i)

    # write ranking
    outRanking = []
    for (id, value) in mcstat.ranking:
        outRanking.append({'uuid':id,'name':players[id]['name'],'value':value})

    with open(dbRankingsPath + '/' + mcstat.name + '.json', 'w') as rankingFile:
        json.dump(outRanking, rankingFile)

# compute and write hall of fame
hof.sort()
outHallOfFame = []
for (id, crown) in hof.ranking:
    if crown[0] == 0:
        break

    outHallOfFame.append({'uuid':id,'name':players[id]['name'],'value':crown})

with open(args.database + '/' + 'hof.json', 'w') as hofFile:
    json.dump(outHallOfFame, hofFile)

# write player data
playerCache = dict()

for uuid, player in players.items():
    playerCache[uuid] = player['name']

    if 'data' in player:
        with open(dbPlayerDataPath + '/' + uuid + '.json', 'w') as dataFile:
            json.dump(player['data'], dataFile)

# write player cache
with open(dbPlayersFilename, 'w') as dbPlayersFile:
    json.dump(playerCache, dbPlayersFile)
