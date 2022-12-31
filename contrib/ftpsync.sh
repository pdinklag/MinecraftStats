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
# script.

. "$(dirname -- "$0")/ftpsync.config" || exit 1

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
