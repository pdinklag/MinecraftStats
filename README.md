# MinecraftStats

[![Example Installation at DVGaming.com](https://img.shields.io/badge/Example-DVGaming.COM%20Snapshot%20Server-blue)](http://mine3.dvgaming.com/)
[![Minecraft 1.13 to 1.17](https://img.shields.io/badge/Minecraft-1.13%20--%201.17-brightgreen)](https://www.minecraft.net/)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://github.com/pdinklag/MinecraftStats/blob/master/LICENSE.txt)
[![Discord](https://img.shields.io/discord/850982115633790976.svg?label=Discord&logo=discord&logoColor=ffffff&color=8399E8&labelColor=7A7EC2)](https://discord.gg/brH5PGG8By)

_MinecraftStats_ is a web browser application for the [statistics](http://minecraft.gamepedia.com/Statistics) that Minecraft servers collect about players.

The presentation is done by giving __awards__ to players for certain achievements. For example, the player who played on the server for the longest total time receives the _Addict_ award. Every award has a viewable ranking associated to it with __medals__ - the award holder gets the gold medal, the second the silver medal and the third the bronze medal for the award. Each medal gives players a __crown score__ (1 for every bronze medal, 2 for every silver, 4 for every gold medal), which is displayed in a server __hall of fame__.

The system is highly customizable. All the awards are defined in Python modules that can be altered, added or removed to fit your needs. Additionally to simply reading Minecraft's original statistics, there are some awards that are combinations of various statistics.

A live demo of _MinecraftStats_ in action is available here: [DVG Snapshot Stats](http://mine3.dvgaming.com/)

Feel free to join the project [Discord](https://discord.gg/brH5PGG8By) 

## Setup Guide
This section describes how to set up _MinecraftStats_ to work on your server.

### Compatibility
_MinecraftStats_ is compatible only to Minecraft 1.13 or later (more precisely: snapshot [17w47a](https://minecraft.gamepedia.com/17w47a) or later).

I am trying to keep the statistics up to date with new Minecraft versions. However, Mojang sometimes decide to rename entity or statistic IDs, which may break some awards. I am trying my best to update accordingly, but please don't hesitate to [open an issue](https://github.com/pdinklag/MinecraftStats/issues) in case you notice something is wrong!

### Requirements
_Python 3.4_ or later is required to feed _MinecraftStats_ with your server's data.

### Installation

I recommend using git to check out the `master` branch of this repository somewhere under your webserver's document root (e.g. `/var/www/html`), as it makes updating easier (see below).

```sh
git clone https://github.com/pdinklag/MinecraftStats.git
```

However, downloading the repository as a zip file and unpacking it there will work as well.

The web application is accessed via `index.html` - so you'll simply need to point your players to the URL corresponding to the installation path.

##### Updating MinecraftStats

To update _MinecraftStats_ to a newer version, if you are using git, the following will do the trick:

```sh
git pull
```

Otherwise, re-download the repository and overwrite any existing files.

### Feeding The Data

The heart of _MinecraftStats_ is the `update.py` script, which loads the player statistics from your Minecraft server into the database for the web application. Said database is file-based and will be stored in the `data` directory by default.

To call the update script, simply go into the installation directory and execute the following:

```sh
python3 update.py config.json
```

When you do this for the first time, the file called `config.json` will be created for you with a default configuration.

You will also receive the following message:

```
server.path not configured, please edit config.json
```

This is because _MinecraftStats_ does not yet know where your Minecraft server is installed. So go ahead and enter the path to your Minecraft server under the `server > path` setting in `config.json`. See below for more configuration possibilities.

### Configuration

The configuration JSON file supprots the following settings:

* `client`
  * `playerCacheUUIDPrefix` - short explanation: *do not touch*. Determines player cache grouping by UUIDs. Most of the time you should leave the default value of 2 untouched. If you have *many* active players on your server (e.g., thousands) and wish to reduce traffic and load times somewhat, you may try increasing this to 3 to see if it helps. Note that increasing this value will increase the number of files under `data/playercache` *exponentially* (!), so handle with care (*default: 2*).
  * `playersPerPage` - how many players to display at most in the players list (*default: 100*).
  * `showLastOnline` - if `true`, the last online date and time will be displayed for players (*default: true*).
* `configVersion` - used internally, do not change manually.
* `crown`
  * `bronze` - the crown score worth of a bronze medal (*default: 1*)
  * `silver` - the crown score worth of a silver medal (*default: 2*)
  * `gold` - the crown score worth of a gold medal (*default: 4*)
* `events` - see below in the *Events* section.
* `players`
  * `exclude` - a list of UUIDs to exclude from the stats (*default: empty*)
  * `excludeBanned` - if `true`, exclude players listed in `banned-players.json` from the stats (*default: true*)
  * `excludeOps` - if `true`, exclude players listed in `ops.json` from the stats (*default: false*)
  * `inactiveDays` - if a player is inactive for this many days, they will no longer be eligible for any awards (*default: 7*)
* `minPlaytime` - only players having played this many minutes or more will be eligible for awards (*default: 0*)
  * `profileUpdateInterval` - update player names and skins using the Mojang API every this many days (*default: 3*)
  * `updateInactive` - also update names and skins of inactive players (not recommended) (*default: false*)
* `server`
  * `sources` - a list of data sources, each of which must define the following
    * `path` - the path to the Minecraft server installation (*no default*)
    * `worldName` the name of the world on the server that contains the player statistics (`stats` directory with JSON files in it). In most cases, this is simply `world` (*default: world*).
  * `customName` - the server name to display on the home page. Leave this at `null` to use the MOTD from your `server.properties` (*default: null*)

##### Combining Multiple Servers

You can combine multiple servers (e.g., servers connected via BungeeCord) into a single stat database by listing multiple entries in the `server` &rarr; `sources` configuration like so:

```json
{
    "server": {
        "sources": [
            {
                "path": "/opt/minecraft/server1",
                "worldName": "world1"
            },
            {
                "path": "/opt/minecraft/server2",
                "worldName": "world2"
            },
        ],
    },
}
```

Any number of servers can be combined this way. Note that *MinecraftStats* will get the server name (MOTD) and icon from the first source only.

##### Migrating Command-Line Configurations

If you have been using _MinecraftStats_ before the configuration was changed to JSON-based, you can use the `makeconfig.py` script with all your old arguments to generate the corresponding JSON configuration, for example:

```sh
python3 makeconfig.py -s /path/to/server --min-playtime 60 > config.json
```

Note that the way how events are started and stopped has changed. You will find the new information in the *Events* section.

#### Troubleshooting

You may encounter the following messages during the update:

* `update.py: error: unrecognized arguments: ...` - if you are sure that everything is right, it may be that when you last used *MinecraftStats*, configuration was still done via the command line. This has changed and you need to switch to the JSON based configuration described above. You can call `makeconfig.py` with the old list of arguments to create a JSON file from it to make the process easier.

* `updating profile for <player> ...` - the updater needs to download the player's skin URL every so often using Mojang's web API ,so that the browser won't have to do it later and slow the web application down. __If this fails__, make sure that Python is able to open `https` connections to `sessionserver.mojang.com`.
* `HTTP Error 429` - Mojang has some limitations on their API that MinecraftStats uses to get player skins. If too many requests for the same player are done within a certain time frame (the exact specs are not known to me), Mojang's API refuses the request with a 429 code. This normally shouldn't happen if you use the default profile update interval.
* `unsupported data version 0 for <player>` - this means that `<player>` has not logged into your server for a long time and his data format is still from Minecraft 1.12.2 or earlier.

In case you encounter any error messages and can't find an explanation, don't hesistate to [open an issue](https://github.com/pdinklag/MinecraftStats/issues).

After the update, you will have a `data` directory that contains everything the web application needs; refer to the *Database Structure* section for details.

### Automatic Updates
_MinecraftStats_ does not include any means for automatic updates - you need to take care of this yourself.

#### Cronjobs

The most common way to do it on Linux servers is by creating a cronjob that starts the update script regularly, e.g., every 10 minutes.

:warning: Note that ​ *MinecraftStats* will produce the output (`data` directory) in the *current working directory*, and not simply where `update.py` is located. This means that your cronjob may have to start with a `cd` to your *MinecraftStats* directory, otherwise the output will be created in the home directory of the cron user.

Typically, a cronjob for *MinecraftStats* will look like this:

```
# update MinecraftStats every 10 minutes
 */10 *  *  *  *  cd /path/to/mcstats ; python3 update.py config.json
```

#### Windows

If you're using Windows to run your server... figure something out! There's probably some task scheduler available that you can use.

### FTP
In case you use FTP to transfer the JSON files to another machine before updating, please note that _MinecraftStats_ uses a JSON file's last modified date in order to determine a player's last play time. Therefore, in order for it to function correctly, the last modified timestamps of the files need to be retained.

### Database Structure
The `data` directory will contain the following after running an update:
* `summary.json.gz` - This is a summary for the web application, containing information about the server and everything needed to display the award listing.
* `server-icon.png` - if your server has an icon, this will be a copy of it. Otherwise, a default icon will be used.
* `events` - contains one JSON file for every event containing player scores.
* `playercache` - cache of player names and skin IDs, grouped by player UUIDs.
* `playerdata` - contains one JSON file for every player, containing information displayed in the player view.
* `playerlist` - contains an index for player information used by the player list.
* `rankings` - contains one JSON file for every award containing player rankings.

## Events
Events allow you to track a specific award stat for a limited amount of time. You can plan events via the `events` list in the config JSON. The following information needs to be specified for an event:

* `name` - the *unique* internal name of the event, which needs to be a valid file and URL name, i.e., you should not use spaces or special characters here. Every event needs a different name, even if they share the same title.
* `title` - the title of the event displayed in the browser.
* `stat` - the ID of the award stat counted for the event. An easy way to find these IDs is by clicking an award in the browser and getting it from the URL.
* `startTime` - the time at which the event starts in `YYYY-MM-DD HH:MM` format (4-digit year followed by 2-digit month, day, hour and minute).
* `endTime` - the time at which the event ends (same format as `startTime`).

When you run `update.py`, events will automatically be started or stopped based on the current server time.

##### Event Example

As an example, let's consider a Halloween-themed event called "Skeleton Hunt" that tracks how many skeletons people kill between October 30, 10 o'clock in the morning and midnight of November 1. We would add the following to the config JSON:

```json
...
	"events": [
        {
            "name": "skeleton_hunt_2020",
            "title": "Skeleton Hunt",
            "stat": "kill_skeleton",
            "startTime": "2020-10-30 10:00",
            "endTime": "2020-01-01 00:00"
        }
    ],
...
```

## Customizing Awards

I assume here that you have some very basic knowledge of Python, however, you may also get away without any.

`update.py` imports all modules from the `mcstats/stats` directory. Here you will find many `.py` files that define the awards in a pretty straightforward way.

Any changes will be in effect the next time `update.py` is executed.

### Adding New Awards
For adding a new award, follow these steps:

1. Create a new module in `mcstats/stats` and register your `MinecraftStat` instances (see below).
2. Place an icon for the award in `img/award-icons`. If your award ID is `my_award`, the icon's file name needs to be `my_award.png`.

#### The MinecraftStat Class
A `MinecraftStat` object consists of an _ID_, some _meta information_ (_title_, _description_ and a _unit_ for statistic values) and a _StatReader_.

The _ID_ is simply the award's internal identifier. It is used for the database and the web application also uses it to locate the award icon (`img/award-icons/<id>.png`).

The _meta information_ is for display in the web application. The following units are supported:
* `int` - a simple integer number with no unit.
* `ticks` - time statistics are usually measured in ticks. The web application will convert this into a human readable duration (seconds, minutes, hours, ...).
* `cm` - Minecraft measures distances in centimeters. The web application will convert this to a suitable metric unit.

The _StatReader_ is responsible for calculating the displayed and ranked statistic value. Most commonly, this simply reads one single entry from a player's statistics JSON, but more complex calculations are possible (e.g., summing up various statistics like for the `mine_stone`.

There are various readers, the usage of which is best explained by having a close look to the existing awards. If you require new types of calculations, dig in the `mcstats/mcstats.py` file and expand upon what's there.

### Modifying and Removing Awards
In order to modify or remove an award, find the corresponding module and modify or delete it to suit your needs.

Note that some awards, e.g., all the mob kill awards, are grouped into a single python file.

## Development Notes
This section contains some hints for those who want to develop on _MinecraftStats_.

### Web Frontend Localization

The web frontend is fully localized. If you cannot find your language yet, please feel very welcome to provide a localization and create a pull request! In order to add a new language, two things have to be done:

* Create a new language JSON file in the `localizations` directory and fill it with your translations. For the file name, please choose the corresponding [ISO 639-1](https://en.wikipedia.org/wiki/ISO_639-1) code for your language.
* Find the `language-dropdown` element in `index.html` and add a new entry for your language there. The text should be the name of the language in that language (e.g. "Deutsch" for German, which is the German word for "German"). Please try and keep the dropdown sorted alphabetically.

### JavaScript and CSS minimization

In an effort to reduce client traffic, the JavaScript and CSS files of the web UI are minified. The JavaScripts are minified using [terser](https://github.com/terser/terser). Refer to the `minimize.sh` script located in the `js` directory for the command-line used to do so. For CSS minimization, I use [uglifycss](https://www.npmjs.com/package/uglifycss) without any special command-line parameters.

## License and Attribution

_MinecraftStats_ is released under the [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) license. This means you can pretty much use and modify it freely, with the only requirements being attribution and not putting it under restrictive (e.g., commercial) licenses if modified.

Concerning the _attribution_ part, the only requirement is that you provide a visible link to [this original repository](https://github.com/pdinklag/MinecraftStats) in your installment. The easiest way to do this is by not removing it from the `index.html` footer, where you will also find a reminder about this.
