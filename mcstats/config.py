defaultConfig = {
    "configVersion": 1,
    "database": "data",              # where the database is written
    "server": {
        "sources": [
            {
                "path": False,       # path to server
                "worldName": "world" # name of the world to use, probably always "world"
            }
        ],
        "customName": False,         # custom server name; use MOTD if empty
    },
    "client": {
        "playersPerPage": 100,       # how many players to display per page
        "playerCacheUUIDPrefix": 2,  # length of UUID prefix for player cache - more = smaller caches
        "showLastOnline": True       # whether to show the last online time in the browser
    },
    "players": {
        "profileUpdateInterval": 3,  # update profile after this many days
        "updateInactive": False,     # also update profile for inactive players
        "inactiveDays": 7,           # number of offline days before a player is considered inactive
        "minPlaytime": 60,           # number of minutes a player must have played before entering stats
        "excludeBanned": True,       # whether or not to exclude banned players
        "excludeOps": False,         # whether or not to exclude ops
        "excludeUUIDs": []           # list of UUIDs to exclude
    },
    "crown": {
        "gold": 4,                   # crown score worth of a gold medal     
        "silver": 2,                 # crown score worth of a silver medal
        "bronze": 1                  # crown score worth of a bronze medal
    },
    "events": [],                    # list of events
}
