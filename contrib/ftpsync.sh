#!/bin/sh

# This script will pull the necessary stats files from a remote or hosted
# Minecraft server using ftp and mirror them locally so that the MinecraftStats
# script can successfully run.
#
# This script requires the `lftp` utility which is almost certainly available
# in your OS package repository.  This tool will only transfer new or changed
# files, making it very efficient and fast on subsequent runs.
#
# Edit the config values in the `ftpsync.config` file and then run this 
# script:

CONFIGFILE="$(dirname $0)/ftpsync.config"

if [ -e $CONFIGFILE ]; then 
    # Configuration file found, load it up
    source $CONFIGFILE
else
    # Cannot find configuration file in expected location
    echo "Configuration file $CONFIGFILE not found"
    exit 1
fi

if [ -z "$MIRRORPATH" ]; then
    echo "Configuration not loaded"
    exit 1
fi

# Sync files group and world readable so that the web server can view them
umask 022

# Create the mirror path if it doesn't already exist
mkdir -p "$MIRRORPATH" || exit 1

# Sync the files from the Minecraft Server
cd "$MIRRORPATH"
lftp -u $FTPUSER,$FTPPASS $FTPHOST -e "mirror -r -I ops.json -I usercache.json -I server.properties -I banned-players.json -I server-icon.png . .; mirror -r $LEVELNAME/stats $LEVELNAME/; mirror -r $LEVELNAME/advancements $LEVELNAME/; bye"

# Run MinecraftStats
cd "$WEBROOT"
python3 update.py config.json
