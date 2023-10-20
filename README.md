# MinecraftStats

[![Minecraft 1.13 to 1.12](https://img.shields.io/badge/Minecraft-1.13%20--%201.20-brightgreen)](https://www.minecraft.net/) [![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://github.com/pdinklag/MinecraftStats/blob/master/LICENSE.txt) [![Example Installation at DVGaming.com](https://img.shields.io/badge/Example-DVGaming.COM%20Snapshot%20Server-blue)](http://mine3.dvgaming.com/) [![Discord](https://img.shields.io/discord/850982115633790976.svg?label=Discord&logo=discord&logoColor=ffffff&color=8399E8&labelColor=7A7EC2)](https://discord.gg/brH5PGG8By)

_MinecraftStats_ is a web browser application for the [statistics](https://minecraft.wiki/w/Statistics) that Minecraft servers collect for players.

The presentation is done by giving __awards__ to players for certain achievements. For example, the player who played on the server for the longest total time receives the _Dedication_ award. Every award has a viewable ranking associated to it with __medals__ - the award holder gets the gold medal, the second the silver medal and the third the bronze medal for the award. Each medal gives players a __crown score__ (1 for every bronze medal, 2 for every silver, 4 for every gold medal), which is displayed in a server __hall of fame__.

A live demo of _MinecraftStats_ in action is available here: [DVG Snapshot Stats](http://mine3.dvgaming.com/). Feel free to join the project's [Discord](https://discord.gg/brH5PGG8By) for help &ndash; or just for fun!

## Overview

This is to give a brief overview as to how *MinecraftStats* works.

### Data Updates

The web frontend of *MinecraftStats* is initially empty and needs to be fed data from your Minecraft server. This is done via an *update*.

The updater (either the plugin or the CLI, see below) will look at your players' statistics, which are typically stored in JSON files under `world/stats` in your Minecraft server's directory. From this, using predefined awards and events, it will compute rankings as well as a Hall of Fame score. The data is contained in a `data` directory in the web frontend's directory.

Using the [Configuration](#configuration), you can change some behaviour like excluding certain players. It is possible to run [Events](#events) that track certain statistics only for a fixed amount of time &ndash; for example, picture a *Skeleton Hunt* event over Halloween. The system is extensible and you can add [Custom Awards](#custom-awards).

### Plugin vs. CLI

*MinecraftStats* comes in two flavors. You can use it as a **Plugin** or via the command-line interface (**CLI**). Briefly, if your server supports plugins (e.g., SpigotMC or PaperMC), using the plugin is the much easier way. If you are running a vanilla server or prefer to have data updates under more careful control, you will have to use the CLI.

This documentation is written for both variants. If anything special applies to one variant in particular, you will always find a corresponding subsection.

#### Plugin Exclusives

The Plugin has some exclusive features, making its use much easier than the CLI. Some features are for communication with other plugins, others are conveniences that are enabled by being run in the scope of a server application.

* Automatic updates at regular intervals.
* Automatic detection of webservers run by other plugins ([dynmap](https://github.com/webbukkit/dynmap)).
* Support for offline-mode skins via [SkinsRestorer](https://skinsrestorer.net/) (v14.2.2 or later).

## Setup

This section will guide you through getting *MinecraftStats* up and running.

### Requirements

*MinecraftStats* supports Minecraft 1.13 or later. For the web frontend, a webserver is required.

#### Plugin

The plugin can be used in any server capable of running Spigot plugins, particularly [Spigot](https://www.spigotmc.org/) or [PaperMC](https://papermc.io/). *MinecraftStats* automatically detects the following plugins that feature a webserver:

* [dynmap](https://github.com/webbukkit/dynmap)
* [BlueMap](https://bluemap.bluecolored.de/)

That said, if you have any of the above plugins installed, there is no need to setup a webserver yourself unless you desire to.

#### CLI

Java 8 or later is required to run the CLI. You will need to setup a webserver yourself.

### Installation

#### Plugin

Simply place `MinecraftStats.jar` into your server's `plugins` directory.

If you intend to use your own webserver, follow the steps described for the [web frontend setup](#web-frontend-setup) below.

#### CLI

Unpack the `MinecraftStatsCLI.zip` from the release wherever you like. In the [Configuration](#configuration), you **must** set the `data → documentRoot` and `server → sources` settings to match your system.

Furthermore, follow the steps described for the [web frontend setup](#web-frontend-setup) below.

##### Combining Multiple Servers (BungeeCord)

The `server → sources` setting supports multiple entries, so you can combine multiple servers into a single statistics browser.

#### Web Frontend Setup

Extract the contents of `MinecraftStatsWeb.zip` to the place within your document root that you configured in the `data → documentRoot` setting.

Make sure that the updater has write permissions to that directory.

#### Migrating from Python

If you previously used the Python version, you can use *MinecraftStats* almost like before by using the CLI. Bascially, `update.py` is now `MinecraftStatsCLI.jar` that you run via `java -jar` rather than Python. Just like for Minecraft 1.13, Java 8 or later is required.

:warning: The former workflow of simply cloning this repository and updating away is now deprecated. The repository only contains the source code, the runnable jar and ready web frontend files must be built from source or can be downloaded from the releases. To migrate, keep your config and follow the steps described for the CLI and Web Frontend above, then do the following config updates.

In your `config.json`, you will now have to add the `data → documentRoot` setting that points to your webserver (see [Configuration](#configuration) for details):

```json
"data": {
    "documentRoot": "/var/www/html"
},
```

The `server → customName` setting has been renamed to `client → serverName`.

If you created custom awards, you will have to translate them to a JSON representation; the Python scripts will no longer work. Head to [Custom Awards](#custom-awards) for details. If you used events, they are no longer stated in `config.json` but in separate files. See [Events](#events) for details.

### Configuration

Depending on whether you use the plugin or the CLI, the configuration is done in a YAML or JSON file, respectively. The following settings apply for both.

* **`data → documentRoot`**: Set this to where the web frontend of *MinecraftStats* resides (e.g., `index.html`). This is where the updater will generate the `data` directory that contains all the data for the web frontend to display. In the plugin, leave this to `null` to make the plugin look for a supported webserver.
* **`data → eventsDir`**: The directory that event definitions are loaded from. See [Events](#events) for details. In the plugin, this is relative to the plugin's directory; in the CLI, this is relative to the location of your `config.json`.

* **`data → statsDir`**: The directory that custom award definitions are loaded from. See [Custom Awards](#) for details. In the plugin, this is relative to the plugin's directory; in the CLI, this is relative to the location of your `config.json`.
* **`crown → bronzeMedal`:** The crown score a player gets in the Hall of Fame for a bronze medal.
* **`crown → silverMedal`:** The crown score a player gets in the Hall of Fame for a silver medal.
* **`crown → goldMedal`:** The crown score a player gets in the Hall of Fame for a gold medal.
* **`client → defaultLanguage`**: The [ISO 639-1](https://en.wikipedia.org/wiki/ISO_639-1) code of the default language to use when none was explicitly selected by the user.
* **`client → playerCacheUUIDPrefix `**:  Short explanation: *do not touch*. Determines player cache grouping by UUIDs. Most of the time you should leave the default value of 2 untouched. If you have *many* active players on your server (e.g., thousands) and wish to reduce traffic and load times somewhat, you may try increasing this to 3 to see if it helps. Note that increasing this value will increase the number of files under `data/playercache` *exponentially* (!), so handle with care.
* **`client → playersPerPage `**: How many players to display at most on one page of the players list.
* **`client → serverName`**: If this is set, this will be shown as the server's name in the web frontend. Leave it to `null` to use the server's MOTD.
* **`client → showLastOnline `**: If set to `true`, the last online date and time will be displayed in the web frontend.
* **`players → excludeBanned `**:  If `true`, exclude banned players from the stats.
* **`players → excludeOps `**:  If `true`, exclude ops from the stats.
* **`players → excludeUUIDs `**:  An array of player UUIDs that will be excluded from the stats.
* **`players → inactiveDays`**: If a player is inactive for this many days, they will no longer be eligible for any awards.
* **`players → minPlaytime `**: Only players who have played at least this many minutes will be considered in the stats.
* **`players → profileUpdateInterval`**: Update player names and skins using the Mojang API every this many days.
* **`players → updateInterval`**: Update names and skins of inactive players.

#### Plugin

The configuration is done in the plugin's `config.yml`. If it does not exist, the default configuration will be created.

The following settings are **for the plugin only**:

* **`data → webSubdir`**: The name of the directory that *MinecraftStats* creates in the webserver's document root. This only applies if `data → documentRoot` is `null` and the plugin found a supported webserver.
* **`data → unpackWebFiles`**: If set to `true`, the plugin will automatically unpack all the necessary files required for the web frontend. This only applies if `data → documentRoot` is `null` and the plugin found a supported webserver. :warning: If you modify the web frontend, set this to `false` to ensure that your changes won't be overridden.
* **`data → updateInterval`**: The data for the web frontend is updated every this many minutes.

#### CLI

The configuration must be given in a JSON file. Edit the default `config.json` to reflect your server.

The following setting is **required for the CLI**:

* **`server → sources`**: An array of data sources, each of which must define the following properties:
* **`path`**: The path to your Minecraft server.
  
* **`worldName`**: the name of the world on the server that contains the player statistics (i.e., the `stats` directory with JSON files in it). In most cases, this is simply `world`.

### Usage

This section describes the everyday use of *MinecraftStats*.

#### Plugin

By installing the plugin with the default configuration and if you have a plugin featuring a webserver (see [Requirements](#requirements)), you're already set. The plugin will automatically update the data for the web frontend once started, and then regularly according to the `data → updateInterval` setting.

If you rely on *MinecraftStats* to find a webserver plugin, this is how you and your players access the web frontend using a browser:

* **dynmap**: Let's say your URL is `my-server.com:8123`, then you access the *MinecraftStats* frontend via `my-server.com:8123/stats/index.html`. Note that due to how dynmap's webserver is configured, you cannot leave the `/index.html` part by default. If you change the `data → webSubdir` setting, the `/stats/` part in the URL must be changed accordingly.
* **BlueMap**: The same as for dynmap applies, but note that the default port there is different. The default URL in BlueMap will be `my-server.com:8100/stats/index.html`.

#### CLI

When using the CLI, the data for the web frontend needs to be updated by executing `MinecraftStatsCLI.jar` like so:

```sh
java -jar MinecraftStatsCLI.jar config.json
```

#### CLI in Docker

Instead of running the CLI on the host you can place it neatly separated into multiple container using Docker.
The [Dockerfile](./Dockerfile) builds the image [chrisbesch/minecraft_stats](https://hub.docker.com/r/chrisbesch/minecraft_stats).
Here is an example deployment using Docker Compose: [example_docker_compose](./example_docker_compose)
Run it with `docker compose up` and you should have a Minecraft Server (on localhost:25565), MinecraftStats with the accompanying Cron job and web server running on [http://localhost:80](http://localhost:80).

##### Automatic Updates

The CLI does not include any means for automatic updates - you need to take care of this yourself. The following lists some possibilities you might have.

The most common way to do automatic updates (on Linux servers) is by creating a cronjob that starts the update script regularly, e.g., every 10 minutes. Typically, a cronjob for *MinecraftStats* will look like this:
```
# update MinecraftStats every 5 minutes
*/5 *  *  *  *  java -jar MinecraftStatsCLI.jar config.json
```
⚠️ Note that cronjobs run in the *current working directory*. It is therefore recommend to state an *absolute* path in the `data → documentRoot` setting.

##### FTP

In case you use FTP to transfer the player's statistics JSON files to another machine before updating, please note that *MinecraftStats* uses a JSON file's last modified date in order to determine a player's last play time. Therefore, in order for it to function correctly, the last modified timestamps of the files need to be retained.

## Events

Events allow you to track a specific award for a limited amount of time. Events are defined in a JSON file each in the `events` directory either in the plugin's directory (or next to `config.json` for the CLI)..

The following information needs to be specified for an event:

* **`name`**: The *unique* (internal) name of the event, which needs to be a valid file and URL name, i.e., you should not use spaces or special characters here. Every event needs a different name, even if they share the same title.

* **`title`**: The title of the event displayed in the browser.

* **`stat`**: The ID of the award stat counted for the event. An easy way to find these IDs is by clicking an award in the browser and getting it from the URL.

* **`startTime`**: The time at which the event starts in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format (e.g., `YYYY-MM-DD HH:MM`, where the hour field assumes a 24h day).

* **`endTime`**: The time at which the event ends (same format as `startTime`).

Be sure to align your start and end times to your update interval in order to avoid inaccuracies.

:warning: Note that **at least one update must happen before the event starts**. Otherwise, there is no way for *MinecraftStats* to know the scores of each player before the event, and thus the scores will be counted from the beginning of the server rather than your start time.

### Example

As an example, consider a Halloween-themed event called "Skeleton Hunt" that tracks how many skeletons people kill between October 30, 10 AM in the morning and midnight of November 1. We would create the file `skeleton-hunt-2023.json` in the `events` directory with the following contents:

```json
{
    "name": "skeleton_hunt_2023",
    "title": "Skeleton Hunt",
    "stat": "kill_skeleton",
    "startTime": "2023-10-30 10:00",
    "endTime": "2023-11-01 00:00"
}
```

## Custom Awards

The awards are defined in the `stats` directoy in a JSON file each. You can create additional awards simply by adding another JSON file. By convention, the name of the JSON file should match the ID of the award.

A JSON object defining an award consists of the following felds:

* **``id`` **: The *unique* ID of the award. This is also the ID that you will later find in the URL in the web frontend. It must be a valid name for a file as well as a portion of a URL, so avoid special characters as well as spaces.
* **`unit`**: The unit in which award scores are measured. The following units commonly occur in Minecraft and are recognized:
  * `int`: A plain integer number (e.g., the number of times a player has done something).
  * `cm`: A number of centimeters, in which Minecraft measures distances (e.g., the distance a player has traveled in some way).
  * `ticks`: A number of ticks, in which Minecraft measures durations (e.g., for how long a player has done something).
  * `tenths_of_heart`: 1/10 of a heart, in which Minecraft measures health and damage (e.g., how much damage was done for something).
* **`reader`**: Defines how data is read from the player statistics JSON files, see [Data Readers](#data-readers) for more information.
* **`minVersion`** (optional): The minimum data version that the server must have in order for this award to be enabled. If the server runs an older version of Minecraft, the award is not included in the web frontend. If no minimum version is specified, the default is 1451, which is the data version of [snapshot 17w47a](https://minecraft.wiki/w/Java_Edition_17w47a), the first version supported by *MinecraftStats*. You can find the data version of a specific Minecraft version by consulting the info panel on a version page in the [Minecraft Wiki](https://minecraft.wiki).

As a hint, if you wish to create a custom award, it is a good idea to find an already existing award that is similar to what you have in mind, and then copy its JSON file and edit it as needed. Especially regarding data readers, this is by far the most simple way that should work for almost all cases.

### Data Readers

Readers define how an award score is determined from a player's statistics JSON. There are different types of readers that can be selected using the **`$type`** field. The other fields that are available depend on the selected type. The following is a listing of the available reader types, each with an example award (ID) for reference.

* **`int`**: Reads a single integer from the nested object given by the `path` array. The final entry in `path` is the name of the field to read. Example: `jump`.
* **`match-sum`**: Reads multiple integers from the nested bject given by `path`. The fields that are read are given in the `patterns` array, which may contain [regular expressions](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html). Example: `break_tools`.
* **`set-count`**: Counts the number of distinct entries in the nested object or array given by `path`. Example: `biomes`.

#### Advancements

*MinecraftStats* also loads players' advancements. These can be accessed by stating `advancements` as the first node. An example can be found in the `biomes` award, which counts the number of different biomes a player has visited.

### Icon

Place your award's icon into the `img/award-icons` directory of the web frontend. It must be named after the award's ID.

### Localization

You give your award a human-readable title and description by editing the localization. The localization files are found in the `localization` directory of the web frontend with one JSON file per language each.

## Development

*MinecraftStats* is a [Gradle](https://gradle.org/) project. By executing the `release` task, all release artifacts (Plugin, CLI and standalone web frontend) are generated from the source.

## Troubleshooting

Here is some help troubleshooting common issues.

* The CLI tells me `org.json.JSONException: JSONObject["data"] not found.`
  * You have likely just migrated from Python and did not configure a document root yet.
* The plugin tells me `No document root specified -- please state one explictly in the configuration, or install a supported plugin featuring a webserver!`
  * You may not have a supported plugin with a webserver installed (see [Requirements](#requirements)). Please install one of those, or set up a webserver by yourself following [Installation](#installation).

* The web frontend is stuck at the loader image and does not show anything.
  * This typically means that the data generated by an update cannot be loaded. Please open the browser console (`F12 → Console` in most browsers) and look for error messages.
  * Any file not found (code 404) errors may hint that data has not been generated. Make sure there is a `data` folder in your webserver's document root. If not, chances are you did not run any update, or the data was written to a wrong location (double-check the configuration).
  * If there is anything logged about a *CORS Policy*, chances are you are trying to open `index.html` from your filesystem directly. As a security measure, most browsers do not support loading JavaScript from the filesystem, hence the frontend will not work. Please use a local webserver instead.
  * In case you have configured your webserver to compress files before transfer to the client, this may cause it to compress the `.json.gz` files of *MinecraftStats* and confuse the frontend, rendering it unable to properly decompress them. Please make sure that there is an exception for `*.gz` files &ndash; they are already compressed!
  * If you're getting an error like this in the browser console `Uncaught incorrect header check` there might not be any active players. Try setting `minPlaytime` to `0` and `inactiveDays` to something large.

## History

The project started as a hyper-casual idea to get player rankings for certain things. It was meant as a special attraction on our small snapshot survival server at [DVGaming](https://dvgaming.com/). Because we ran snapshot versions of Minecraft, vanilla servers had to be supported and thus a plugin for Bukkit was out of question. The project was a very simple command-line script in the beginning, and I chose Python to do that.

*MinecraftStats* was rewritten twice. The first rewrite happened in 2018 following the release of [snapshot 17w47a](https://minecraft.wiki/w/Java_Edition_17w47a) for Minecraft 1.13, where Mojang change the structure of how Minecraft stores player statistics completely.

Throughout the years, *MinecraftStats* gained some popularity, much more than anticipated. With that, requests for a Bukkit (Spigot / PaperMC) plugin became more frequent. A first shot at a plugin that simply executed the Python script failed, because many hosters don't allow that. For that reason, and to reflect the fact that the project had become much more complex and the Python code became more and more of a mess, the project was rewritten in Java in a way that both plugin and vanilla servers are supported.

Only since the Java implementation, *MinecraftStats* officially has numbered versions that follow the [Semantic Versioning](https://semver.org/) scheme.

## Changelog

### 3.2.1

This update fixes future events being displayed as "Finished" in the web frontend, as well as the "Invalid Date" display for event end times.

### 3.2.0

This update adds automatic detection of BlueMap's webserver and fixes bugs in the plugin.

* Additionally to dynmap, the plugin now also detects the webserver of [BlueMap](https://bluemap.bluecolored.de/).
* Fixed the `data → unpackWebFiles` being ignored.
* Fixed an issue with non-ASCII characters in generated JSON files, color-coded server MOTDs should now work again.

### 3.1.0

This update adds SkinsRestorer for the plugin and avoids unnecessary Mojang API calls.

* The plugin can now get skins from [SkinsRestorer](https://skinsrestorer.net/) v14.2.2 or later.
* If a player is detected to be an offline player (e.g., Floodgate players or if the Mojang API gave an empty response), no further attempts at asking the Mojang API will be made.
* Minimized the log output of the plugin.

### 3.0.2

This patch release fixes issues that occurred for offline-mode servers.

- The message logged when a player's UUID cannot be found by Mojang's API is now less scary.
- The plugin now gets dynmap's actual `webpath` rather than assuming it to be "web".
- Fixed a player's default name being their UUID, which causes their name never to be updated if they cannot be found by Mojang's API.

### 3.0.1

In full 202X fashion, here's a release-day patch that fixes an issue in the plugin. The CLI and web frontend are not affected.

- The plugin now gets the default world's actual name from the Bukkit server rather than assuming it to be `world`.

### 3.0.0

This was the initial release of the Java reimplementation.

## License and Attribution

*MinecraftStats* is released under the [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) license. This means you can pretty much use and modify it freely, with the only requirements being attribution and not putting it under restrictive licenses if modified.

The only requirement regarding *attribution* is that you provide a visible link to [this original repository](https://github.com/pdinklag/MinecraftStats) in your installment. The easiest way to do this is by not removing it from the footer in `index.html` where you will also find a reminder about this.
