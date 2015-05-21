# MinecraftStats

_MinecraftStats_ is a PHP-based browser for all those [stats][1] that Minecraft servers collect about players.

The presentation is done by giving __awards__ to players for certain achievements. For example, the player who cut the most trees in the game gets the _Woodcutter_ award. Every award has a viewable ranking associated to it with __medals__ - the award holder gets the gold medal, the second the silver medal and the third the bronze medal for the award. Each medal gives players a __crown score__ (1 for every bronze medal, 2 for every silver, 4 for every gold medal), the player with the highest crown score is declared __King__ of the server! (sorry girls, I would introduce a Queen, but Minecraft holds no gender information)

The system is highly customizable. All the awards are defined in a single huge PHP script that can be modified to fit your needs. Additionally to simply reading Minecraft's original stats, there are some awards that are combinations of various stats.

A live demo of _MinecraftStats_ in action is here: [DVG Snapshot Stats][2]

## Setup Guide

### Requirements

You need a webserver that does PHP 5.4 or later. Make sure you enable [short open tags][3]. For updating the stat info from your Minecraft server (see below), I recommend the PHP CLI (Linux users install `php5-cli`, Windows users can simply use `php.exe`).

Also note that _MinecraftStats_ was designed for Linux systems - because updating the stats info (see below) is easiest done using a cronjob. It will work fine in Windows, of course, but then it's your problem to find a way to invoke updates automatically and regularly. More info on this below.

### Installation
Simply checkout this repository somewhere in your webserver's document root (e.g. `htdocs/MinecraftStats`). Create an empty directory named `data` and make sure the webserver has write rights on it. This is where _MinecraftStats_ will put its caches when updating.

### Feeding the data
Minecraft stores its statistics in the many JSON files under `world/stats` (this is valid for vanilla servers, I cannot speak for Bukkit or other modded servers, but it should be similar). That's the only data source that _MinecraftStats_ needs. However, it is _not_ a live browser. Instead, the info is cached in a custom format so the site can be displayed efficiently. This means that _MinecraftStats_ needs to be fed with up-to-date data regularly.

First, create a directory named `raw` in your _MinecraftStats_ directory. The following steps are then used to update _MinecraftStats_' data:
1. Copy the JSON files from `<Minecraft server dir>/world/stats` into the `raw` directory.
2. Run `php update.php` in a command shell [*]. __Note:__ If you have an established server with many players, the initial update may take a long time. This is because _MinecraftStats_ is retrieving the players' skin URLs using Mojang's web API.

Step one is necessary, because if we just used the original JSON files as the data source, they may change while the update is running. This might result in read/write conflicts as well as inconsistencies. So better just create a copy.

This update procedure is best done regularly using a simple cronjob-controlled script (Windows users may try using the task scheduler). On my server, I do this every 10 minutes, which is fairly reasonable.

[*] _I recommend using the PHP CLI, but you can also just call up `update.php` in your browser. However, you will not get any progress information and if it takes longer, the browser may hang up because it thinks the site timed out. It's also bad if you need to do it manually all the time._

### General configuration
Configuration is done in `config.php`. It contains a bunch of settings, some of which are explained below. Those that aren't explained are changed at your own risk.

__General settings:__
* `$title` - it's the title of the page. Best change this to your server's name.
* `$inactiveTime` - the amount of time (in seconds) after which players are marked as _inactive_ if they do not log in during that time. Inactive players are not eligible to get any awards. Default is seven days.
* `$itemsPerPage` - pretty much self-explanatory.
* _Time Zone_ - change this to your server's time zone. This is merely for display on the bottom of the page, but it avoids confusion for people browsing the stats. Here's a list of time zones supported by PHP: [http://php.net/manual/en/timezones.php]

__Hall of Fame settings:__
* `$goldMedalScore` - the crown score amount gained for a gold medal.
* `$silverMedalScore` - the crown score amount gained for a silver medal.
* `$bronzeMedalScore` - the crown score amount gained for a bronze medal.

### Award configuration
The huge `$stats` array defined at the end of `config-stats.php` determines what awards there are and how they work. I recommend giving a custom prefix (e.g. `custom.`, duh) to stats that you invented yourself. The `achievement.`, `minecraft.` and `stat.` stats come from Minecraft directly.

Awards support the following fields:
* `award` - the award's name displayed on the site.
* `desc` - a short description of the award, which should follow a simple _<something> <performed action>_ pattern (e.g. _Tools crafted_, _Animals bred_, etc).
* `icon` _[optional]_ - the path to the icon used for this award. This is always relative to the `img/icons` directory. If no icon is specified, a default question mark icon will be used.
* `displayFunc` _[optional]_ - name of the PHP function to format the raw stat value for display. A good use case are the distance stats (e.g. _Distance walked_). Minecraft measures distances in centimeters, but we want to display something human readable, which the function `cmToDistance` takes care of in this case.
* `provider` _[optional]_ - name of the PHP function that reads the stat value from the player's JSON. This is useful for custom stats like _Meat items eaten_: the provider function `eatMeatProvider` gathers multiple stats for eaten items and sums them up into one value. If no provider is given, the stat value is read directly from the JSON using the same array key as the award's key. Of course, this only works for the original stats.

A little tip: if you want to create your own combinated awards, have a look at a player's raw stat data using the _view raw data_ link on his profile page. It helps getting an idea of what data there is, and it's far easier to read than the raw JSON...

## The Suspect award
The _Suspect_ award is a somewhat scientific attempt to find out if somebody may be griefing.

The `suspectProvider` function tests several statistics of a player in order to give him a score of suspiciousness. For example, if a player has placed an enchanting table, but he never mined any obsidian, that makes him suspicious. If he broke a lot more chests than he ever crafted, that makes him even more suspicious.

Of course, there is teamplay and the longer somebody has played on the server, the more obscure this score becomes. So a high suspect score does _not_ mean that somebody is griefing, hence the name _Suspect_. Therefore,  a little advice: handle with care! Use this award as a _hint_ to have a closer look at players, not as a _reason_ to ban players.

[1]:http://minecraft.gamepedia.com/Statistics
[2]:http://dvgaming.com/mcstats/snapshot/
[3]:http://php.net/manual/de/ini.core.php#ini.short-open-tag
