#!/bin/sh

# This script will pull the necessary stats files from a remote or hosted
# Minecraft server using ftp and mirror them locally so that the MinecraftStats
# script can successfully run.
#
# This script requires the `lftp` utility which is almost certainly available
# in your OS package repository.  This tool will only transfer new or changed
# files, making it very efficient and fast on subsequent runs.
#
# Update the values below to your local environment and you should be good
# to go!
#

# Location of MinecraftStats webroot
WEBROOT=/var/www/MinecraftStats

# Target destination for synched files from Minecraft server
MIRRORPATH=/var/minecraft/serverroot

# Minecraft server "level-name" in server.properties (usually "world")
LEVELNAME='world'

FTPHOST=ftp.example.com
FTPUSER=username
FTPPASS=password

# Sync files group and world readable so that the web server can view them
umask 022

# Create the mirror path if it doesn't already exist
mkdir -p "$MIRRORPATH"

# Sync the files from the Minecraft Server
cd "$MIRRORPATH"
lftp -u $FTPUSER,$FTPPASS $FTPHOST -e "mirror -r -I ops.json -I usercache.json -I server.properties -I banned-players.json -I server-icon.png . .; mirror -r $LEVELNAME/stats $LEVELNAME/; mirror -r $LEVELNAME/advancements $LEVELNAME/; bye"

# Run MinecraftStats
cd "$WEBROOT"
python3 update.py config.json
