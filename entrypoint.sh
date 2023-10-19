#!/bin/sh
# This is the entrypoint for the Docker installation.
# It waits patiently for a SIGHUP from the DockerCron container.
# Once it receives one it performs an update.

echo 'copy static html files into /app/www'
mkdir -p /app/www
cp -fr /app/raw_www/* /app/www

echo 'running initial update after boot'
java -jar /app/MinecraftStatsCLI.jar /app/config.json || true

# make sure that you don't `set -e` because that causes the trap to exit the script
# await SIGHUP and then run the actual job
trap 'java -jar /app/MinecraftStatsCLI.jar /app/config.json' HUP
while :; do
    sleep 10 & wait ${!}
done
