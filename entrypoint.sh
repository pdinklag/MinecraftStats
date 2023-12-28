#!/bin/sh
# This is the entrypoint for the Docker installation.
# It waits patiently for a SIGHUP from the DockerCron container.
# Once it receives one it performs an update.

mkdir -p /app/www
# only copy the localization files if /app/www is empty
if [ -z "$(ls -A /app/www)" ]; then
    echo 'copy static html files into /app/www'
    cp -fr /app/raw_www/* /app/www
else
    echo '/app/www is already filled; delete that dir to repopulate'
fi

echo 'copy stat files into /app/stats'
mkdir -p /app/stats
cp -fr /app/raw_stats/* /app/stats

echo 'running initial update after boot'
java -jar /app/MinecraftStatsCLI.jar /app/config.json || true

# make sure that you don't `set -e` because that causes the trap to exit the script
# await SIGHUP and then run the actual job
trap 'java -jar /app/MinecraftStatsCLI.jar /app/config.json' HUP
while :; do
    sleep 10 & wait ${!}
done
