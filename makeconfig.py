#!/usr/bin/env python3
import argparse
import os
import json
import sys

from mcstats import config
from mcstats.util import handle_error
from mcstats.util import merge_dict

parser = argparse.ArgumentParser(description='Create a MinecraftStats configuration using legacy parameters')
parser.add_argument('--server', '-s', type=str, required=False, default=None,
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
parser.add_argument('--save-config', type=str, required=False, default=None,
                    help='saves the command-line into a config file with the given name (DEFUNCT)')
parser.add_argument('--load-config', '-c', type=str, required=False, default=None,
                    help='uses the command-line from the config file with the given name')

args = parser.parse_args()

cfgPath = 'config/'
if args.load_config:
    # try to load config
    cfgFilename = cfgPath + args.load_config
    if os.path.isfile(cfgFilename):
        with open(cfgFilename, 'r') as cfgFile:
            cfg = cfgFile.read().splitlines()

        args = parser.parse_args(cfg + sys.argv[1:]) # append current command-line arguments to loaded config
    else:
        handle_error('configuration not found: ' + args.load_config, True)

# create a JSON config and dump it to stdout
configJson = config.defaultConfig
merge_dict(configJson, {
    "server": {
        "sources": [
            {
                "path": args.server,
                "worldName": args.world,
            }
        ],
        "customName": args.server_name,
    },
    "client": {
        "playersPerPage": args.players_per_page,
        "playerCacheUUIDPrefix": args.player_cache_q,
    },
    "players": {
        "profileUpdateInterval": args.profile_update_interval,
        "updateInactive": args.update_inactive,
        "inactiveDays": args.inactive_days,
        "minPlaytime": args.min_playtime,
    },
    "crown": {
        "gold": args.crown_gold,
        "silver": args.crown_silver,
        "bronze": args.crown_bronze
    },
})

print(json.dumps(configJson, indent=4))
