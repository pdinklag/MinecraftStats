package de.pdinklag.mcstats;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONObject;

import de.pdinklag.mcstats.util.ResourceUtils;
import de.pdinklag.mcstats.util.ClientUtils;
import de.pdinklag.mcstats.util.FileUtils;
import de.pdinklag.mcstats.util.MinecraftServerUtils;
import de.pdinklag.mcstats.util.StreamUtils;

/**
 * The heart of MinecraftStats.
 */
public abstract class Updater {
    private static final String JSON_FILE_EXT = ".json";
    private static final int MIN_DATA_VERSION = 1451; // 17w47a
    private static final String DATABASE_PLAYERS_JSON = "players.json";
    private static final String DATABASE_EVENTS = "events";
    private static final String DATABASE_RANKINGS = "rankings";
    private static final String DATABASE_PLAYERCACHE = "playercache";
    private static final String DATABASE_PLAYERDATA = "playerdata";
    private static final String DATABASE_PLAYERLIST = "playerlist";
    private static final String DATABASE_PLAYERLIST_ALL_FORMAT = "all%d.json.gz";
    private static final String DATABASE_PLAYERLIST_ACTIVE_FORMAT = "active%d.json.gz";
    private static final String DATABASE_SUMMARY = "summary.json.gz";

    private static final String EVENT_INITIAL_SCORE_FIELD = "initialRanking";

    private static final int MINUTES_TO_TICKS = 60 * MinecraftServerUtils.TICKS_PER_SECOND;

    private static final long DAYS_TO_MILLISECONDS = 24L * 60L * 60L * 1000L;

    // initialization
    protected final Config config;
    protected final LogWriter log;

    // protected final LinkedList<PlayerFilter> playerFilters = new LinkedList<>();
    // protected final PlayerFilter inactiveFilter;
    private final HashMap<String, Stat> awards = new HashMap<>();

    // protected final LinkedList<PlayerProfileProvider> localProfileProviders = new LinkedList<>();
    // private final PlayerProfileProvider authenticProfileProvider;

    // paths
    private final Path dbPath;
    private final Path dbPlayersJsonPath;
    private final Path dbEventsPath;
    private final Path dbRankingsPath;
    private final Path dbPlayercachePath;
    private final Path dbPlayerdataPath;
    private final Path dbPlayerlistPath;

    protected PlayerProfileProvider getAuthenticProfileProvider() {
        return new MojangAPIPlayerProfileProvider();
    }

    protected void gatherLocalProfileProviders(PlayerProfileProviderList providers) {
        // usercache.json
        config.getDataSources().forEach(source -> {
            Path usercachePath = MinecraftServerUtils.getUserCachePath(source.getServerPath());
            if (Files.isRegularFile(usercachePath)) {
                try {
                    JSONArray usercacheJson = new JSONArray(Files.readString(usercachePath));
                    providers.add(new UserCachePlayerProfileProvider(usercacheJson));
                } catch (Exception e) {
                    log.writeError("failed to read usercache: " + usercachePath.toString(), e);
                }
            }
        });
    }
    
    private PlayerProfileProvider getLocalProfileProvider() {
        PlayerProfileProviderList providers = new PlayerProfileProviderList();
        gatherLocalProfileProviders(providers);

        // players.json
        if (Files.isRegularFile(dbPlayersJsonPath)) {
            try {
                JSONObject playersJson = new JSONObject(Files.readString(dbPlayersJsonPath));
                providers.addFirst(new DatabasePlayerProfileProvider(playersJson));
            } catch (Exception e) {
                log.writeError("failed to load players from previous database: " + dbPlayersJsonPath.toString(), e);
            }
        }
        return providers;
    }

    protected PlayerFilter getHardPlayerFilter() {
        PlayerFilterList filters = new PlayerFilterList();

        // filter players whose data version is too low
        filters.add(new DataVersionPlayerFilter(MIN_DATA_VERSION, Integer.MAX_VALUE));

        // filter players who didn't play long enough
        filters.add(new MinPlaytimePlayerFilter(MINUTES_TO_TICKS * config.getMinPlaytime()));

        // exclude banned players
        if (config.isExcludeBanned()) {
            config.getDataSources().forEach(source -> {
                Path bannedPlayersPath = MinecraftServerUtils.getBannedPlayersPath(source.getServerPath());
                if (Files.isRegularFile(bannedPlayersPath)) {
                    try {
                        JSONArray ops = new JSONArray(Files.readString(bannedPlayersPath));
                        filters.add(new JSONPlayerFilter(ops));
                    } catch (Exception e) {
                        log.writeError("failed to read banned players file: " + bannedPlayersPath.toString(), e);
                    }
                }
            });
        }

        // exclude ops
        if (config.isExcludeOps()) {
            config.getDataSources().forEach(source -> {
                Path opsPath = MinecraftServerUtils.getOpsPath(source.getServerPath());
                if (Files.isRegularFile(opsPath)) {
                    try {
                        JSONArray ops = new JSONArray(Files.readString(opsPath));
                        filters.add(new JSONPlayerFilter(ops));
                    } catch (Exception e) {
                        log.writeError("failed to read ops file: " + opsPath.toString(), e);
                    }
                }
            });
        }

        // filter explicitly excluded players
        if (!config.getExcludeUUIDs().isEmpty()) {
            ExcludeUUIDPlayerFilter filter = new ExcludeUUIDPlayerFilter();
            filter.excludeAll(config.getExcludeUUIDs());
            filters.add(filter);
        }
        return filters;
    }

    protected PlayerFilter getInactiveFilter() {
        // filter players who are inactive
        return new LastOnlinePlayerFilter(System.currentTimeMillis() - DAYS_TO_MILLISECONDS * (long) config.getInactiveDays());
    }

    private HashMap<String, Player> processPlayers(PlayerFilter filter) {
        HashMap<String, Player> discoveredPlayers = new HashMap<>();

        // discover players in data sources
        config.getDataSources().forEach(source -> {
            Path statsPath = source.getPlayerStatsPath();
            Path advancementsPath = source.getPlayerAdvancementsPath();
            try {
                Files.list(statsPath).forEach(path -> {
                    try {
                        final String filename = path.getFileName().toString();
                        if (Files.isRegularFile(path) && filename.endsWith(JSON_FILE_EXT)) {
                            // extract UUID from filename
                            final String uuid = filename.substring(0, filename.length() - JSON_FILE_EXT.length());

                            // read JSON
                            final JSONObject statsRoot = new JSONObject(Files.readString(path));
                            final JSONObject stats =  statsRoot.getJSONObject("stats");

                            // read advancements if present
                            final Path advancementsJsonPath = advancementsPath.resolve(filename);
                            if(Files.exists(advancementsJsonPath)) {
                                final JSONObject advancements = new JSONObject(Files.readString(advancementsJsonPath));
                                stats.put("advancements", advancements);
                            }

                            // gather basic information
                            Player player = discoveredPlayers.getOrDefault(uuid, new Player(uuid));

                            final long lastOnlineTime = Files.getLastModifiedTime(path).toMillis();
                            player.setLastOnlineTime(Math.max(player.getLastOnlineTime(), lastOnlineTime));

                            final int dataVersion = DefaultReaders.DATA_VERSION_READER.read(statsRoot).toInt();
                            player.setDataVersion(Math.max(player.getDataVersion(), dataVersion));

                            final int playTime = DefaultReaders.PLAYTIME_READER.read(stats).toInt();
                            player.setPlaytime(Math.max(player.getPlaytime(), playTime));

                            // gather stats
                            player.getStats().gather(awards.values(), stats, dataVersion);

                            // register in set of players
                            discoveredPlayers.put(uuid, player);
                        }
                    } catch (Exception e) {
                        log.writeError("failed to process file: " + path.toString(), e);
                    }
                });
            } catch (IOException e) {
                log.writeError("failed to run discovery on data source: " + statsPath.toString(), e);
            }
        });

        // filter players
        HashMap<String, Player> filteredPlayers = new HashMap<>();
        discoveredPlayers.forEach((uuid, player) -> {
            if(filter.filter(player)) filteredPlayers.put(uuid, player);
        });

        return filteredPlayers;
    }

    private void writePlayerList(Collection<Player> players, String filenameFormat) {
        final ArrayList<Player> playersSorted = new ArrayList<>(players);
        Collections.sort(playersSorted, (a, b) -> a.getProfile().getName().compareToIgnoreCase(b.getProfile().getName()));

        final int playersPerPage = config.getPlayersPerPage();
        final int numPlayers = players.size();
        final int numPages = (int) Math.ceil((double) numPlayers / playersPerPage);

        for (int pageNum = 0; pageNum < numPages; pageNum++) {
            final int first = pageNum * playersPerPage;
            final int last = Math.min(first + playersPerPage, numPlayers);

            final JSONArray page = new JSONArray(playersPerPage);
            for (var i = first; i < last; i++) {
                page.put(playersSorted.get(i).getClientInfo(true));
            }

            final Path pageFilePath = dbPlayerlistPath.resolve(String.format(filenameFormat, pageNum + 1));
            try {
                FileUtils.writeStringGzipped(pageFilePath, page.toString());
            } catch (IOException e) {
                log.writeError("failed to write playerlist page file: " + pageFilePath, e);
            }
        }
    }

    public Updater(Config config, LogWriter log) {
        this.config = config;
        this.log = log;

        // cache some paths
        this.dbPath = config.getDatabasePath();
        this.dbPlayersJsonPath = dbPath.resolve(DATABASE_PLAYERS_JSON);
        this.dbEventsPath = dbPath.resolve(DATABASE_EVENTS);
        this.dbRankingsPath = dbPath.resolve(DATABASE_RANKINGS);
        this.dbPlayercachePath = dbPath.resolve(DATABASE_PLAYERCACHE);
        this.dbPlayerdataPath = dbPath.resolve(DATABASE_PLAYERDATA);
        this.dbPlayerlistPath = dbPath.resolve(DATABASE_PLAYERLIST);

        // discover and instantiate stats
        try {
            ResourceUtils.getResourceFilenames(getClass().getClassLoader(), "stats").forEach(resource -> {
                try {
                    final JSONObject obj = new JSONObject(
                            StreamUtils.readStreamFully(getClass().getResourceAsStream(resource)));
                    
                    final Stat stat = StatParser.parse(obj);
                    if(!awards.containsKey(stat.getId())) {
                        awards.put(stat.getId(), stat);
                    } else {
                        log.writeLine("duplicate stat id \"" + stat.getId() + "\"");
                    }
                } catch (Exception e2) {
                    log.writeError("failed to load stat from resources: " + resource, e2);
                }
            });
        } catch (Exception e) {
            log.writeError("failed to discover stats", e);
        }
    }
    
    /**
     * Gets the server's message of the day.
     * @return the server's message of the day
     */
    protected abstract String getServerMotd();

    public void run() {
        // get current timestamp
        final long now = System.currentTimeMillis();

        // create database directories
        try {
            Files.createDirectories(dbPath);
        } catch (Exception e) {
            log.writeError("failed to create database directories: " + dbPath.toString(), e);
        }

        // discover and process players
        HashMap<String, Player> allPlayers = processPlayers(getHardPlayerFilter());

        // find effective server version
        final int serverDataVersion;
        {
            int maxDataVersion = 0;
            for (Player player : allPlayers.values()) {
                maxDataVersion = Math.max(maxDataVersion, player.getDataVersion());
            }
            serverDataVersion = maxDataVersion;
        }

        // update player profiles and filter valid players
        PlayerFilter inactiveFilter = getInactiveFilter();
        PlayerProfileProvider localProvider = getLocalProfileProvider();
        PlayerProfileProvider authenticProvider = getAuthenticProfileProvider();
        
        ArrayList<Player> activePlayers = new ArrayList<>();
        ArrayList<Player> validPlayers = new ArrayList<>();
        allPlayers.forEach((uuid, player) -> {
            // use local sources
            player.setProfile(localProvider.getPlayerProfile(player));

            // filter valid players
            final boolean isValid = player.getProfile().hasName();
            if(isValid) {
                validPlayers.add(player);
            }

            // filter active players
            final boolean isActive = inactiveFilter.filter(player);
            if (isActive) {
                activePlayers.add(player);
            }

            // use authentic sources if due
            if (!isValid || isActive || config.isUpdateInactive()) {
                final long updateInterval = DAYS_TO_MILLISECONDS * (long) config.getProfileUpdateInterval();
                final long timeSinceUpdate = now - player.getProfile().getLastUpdateTime();
                if (timeSinceUpdate >= updateInterval) {
                    log.writeLine("updating profile for " + player.getUuid() + " ...");
                    player.setProfile(authenticProvider.getPlayerProfile(player));

                    if(!isValid && player.getProfile().hasName()) {
                        // player has become valid
                        validPlayers.add(player);
                    }
                }
            }
        });

        // write database
        try {
            // create directories
            Files.createDirectories(dbRankingsPath);
            Files.createDirectories(dbEventsPath);
            Files.createDirectories(dbPlayercachePath);
            Files.createDirectories(dbPlayerdataPath);
            Files.createDirectories(dbPlayerlistPath);

            // compute and write rankings
            HashMap<Stat, Ranking<IntValue>.Entry> awardWinners = new HashMap<>();
            awards.forEach((id, award) -> {
                if (award.isVersionSupported(serverDataVersion)) {
                    // rank players
                    final Ranking<IntValue> ranking = new Ranking<IntValue>(activePlayers, player -> {
                        return new IntValue(player.getStats().get(award).toInt());
                    });

                    // notify players of their rankings
                    List<Ranking<IntValue>.Entry> rankingEntries = ranking.getOrderedEntries();
                    for (int rank = 0; rank < rankingEntries.size(); rank++) {
                        final Ranking<IntValue>.Entry e = rankingEntries.get(rank);
                        e.getPlayer().getStats().setRank(award, rank + 1);
                    }

                    // store best for front page
                    if (rankingEntries.size() > 0) {
                        awardWinners.put(award, rankingEntries.get(0));
                    }

                    // write award summary file
                    Path awardJsonPath = dbRankingsPath.resolve(id + JSON_FILE_EXT);
                    try {
                        Files.writeString(awardJsonPath, ranking.toJSON().toString());
                    } catch (Exception e) {
                        log.writeError("failed to write award data: " + awardJsonPath, e);
                    }
                } else {
                    log.writeLine("award " + id + " is not supported by server (data version "
                            + serverDataVersion + ")");
                }
            });

            // process events
            HashMap<Event, Ranking<IntValue>.Entry> eventWinners = new HashMap<>();
            config.getEvents().forEach(event -> {
                if(!event.hasEnded(now)) {
                    final Stat linkedStat = awards.get(event.getLinkedStatId());
                    if(linkedStat != null) {
                        final Path eventDataPath = dbEventsPath.resolve(event.getId() + JSON_FILE_EXT);

                        final JSONObject eventData = new JSONObject();
                        eventData.put("name", event.getId());
                        eventData.put("title", event.getTitle());
                        eventData.put("startTime", ClientUtils.convertTimestamp(event.getStartTime()));
                        eventData.put("endTime", ClientUtils.convertTimestamp(event.getEndTime()));
                        eventData.put("link", linkedStat.getId());

                        if(event.hasStarted(now)) {
                            // the event is currently running, read initial scores and update ranking
                            log.writeLine("updating ranking for event " + event.getId());

                            if(Files.exists(eventDataPath)) {
                                try {
                                    final JSONObject initialRanking = new JSONObject(Files.readString(eventDataPath)).getJSONObject(EVENT_INITIAL_SCORE_FIELD);
                                    event.setInitialScores(initialRanking);
                                    eventData.put(EVENT_INITIAL_SCORE_FIELD, initialRanking);
                                } catch(Exception e) {
                                    log.writeError("failed to load initial scores for event " + event.getId(), e);
                                    eventData.put(EVENT_INITIAL_SCORE_FIELD, new JSONObject());
                                }
                            } else {
                                log.writeLine("event is already running, but no initial scores are available: " + event.getId());
                                eventData.put(EVENT_INITIAL_SCORE_FIELD, new JSONObject());
                            }

                            final Ranking<IntValue> eventRanking = new Ranking<IntValue>(validPlayers, player -> {
                                return new IntValue(player.getStats().get(linkedStat).toInt() - event.getInitialScore(player));
                            });
                            eventData.put("ranking", eventRanking.toJSON());

                            // store best for front page
                            List<Ranking<IntValue>.Entry> rankingEntries = eventRanking.getOrderedEntries();
                            if (rankingEntries.size() > 0) {
                                eventWinners.put(event, rankingEntries.get(0));
                            }
                        } else {
                            // the event has not yet started, update initial scores
                            log.writeLine("updating initial scores for event " + event.getId());
                            
                            final JSONObject initialScores = new JSONObject();
                            allPlayers.forEach((uuid, player) -> {
                                final int score = player.getStats().get(linkedStat).toInt();
                                if(score > 0) initialScores.put(uuid, score);
                            });
                            eventData.put(EVENT_INITIAL_SCORE_FIELD, initialScores);
                        }

                        try {
                            Files.writeString(eventDataPath, eventData.toString());
                        } catch(Exception e) {
                            log.writeError("error writing data for event " + event.getId(), e);
                        }
                    } else {
                        log.writeLine("linked stat \"" + event.getLinkedStatId() + "\" does not exist for event: " + event.getId());
                    }
                }
            });

            // write playerdata
            allPlayers.forEach((uuid, player) -> {
                Path playerdataPath = dbPlayerdataPath.resolve(uuid + JSON_FILE_EXT);
                try {
                    Files.writeString(playerdataPath, player.getStats().toJSON().toString());
                } catch (Exception ex) {
                    log.writeError("failed to write player data: " + playerdataPath, ex);
                }
            });

            // write players.json for next update
            Files.writeString(dbPlayersJsonPath,
                    DatabasePlayerProfileProvider.createDatabase(validPlayers).toString());

            // write playerlist
            writePlayerList(validPlayers, DATABASE_PLAYERLIST_ALL_FORMAT);
            writePlayerList(activePlayers, DATABASE_PLAYERLIST_ACTIVE_FORMAT);

            // write playercache
            {
                final int prefixLength = config.getPlayerCacheUUIDPrefix();
                final HashMap<String, JSONArray> playerCache = new HashMap<>();
                validPlayers.forEach(player -> {
                    final String prefix = player.getUuid().substring(0, prefixLength);

                    JSONArray group = playerCache.get(prefix);
                    if (group == null) {
                        group = new JSONArray(1);
                        playerCache.put(prefix, group);
                    }
                    group.put(player.getClientInfo(true));
                });

                playerCache.forEach((prefix, cache) -> {
                    final Path groupPath = dbPlayercachePath.resolve(prefix + JSON_FILE_EXT);
                    try {
                        Files.writeString(groupPath, cache.toString());
                    } catch (IOException e) {
                        log.writeError("failed to write playerache file: " + groupPath, e);
                    }
                });
            }

            // crown ranking for Hall of Fame
            final Ranking<CrownScoreValue> hallOfFameRanking;
            {
                hallOfFameRanking = new Ranking<CrownScoreValue>(activePlayers, player -> {
                    return player.getStats().getCrownScore(config);
                });
            }

            // write summary
            {
                final JSONObject summary = new JSONObject();
                final HashSet<Player> summaryRelevantPlayers = new HashSet<>();

                final JSONObject info = new JSONObject();
                {
                    // determine the server name
                    String serverName = config.getCustomName();
                    if (serverName == null) {
                        // try all data sources for a server.properties file
                        serverName = getServerMotd();
                        if (serverName != null) {
                            serverName = serverName.replace("\\n", "<br>");
                        }
                        
                        if (serverName == null) {
                            serverName = "";
                            log.writeLine(
                                    "the server's name could not be determined -- try stating a customName in the config");
                        }
                    }

                    // find and copy the server's icon, if any
                    boolean hasIcon = false;
                    for (DataSource dataSource : config.getDataSources()) {
                        final Path iconPath = MinecraftServerUtils.getServerIconPath(dataSource.getServerPath());
                        if (Files.exists(iconPath)) {
                            try {
                                Files.copy(iconPath, dbPath.resolve(iconPath.getFileName()),
                                        StandardCopyOption.REPLACE_EXISTING);
                                hasIcon = true;
                                break;
                            } catch (Exception e) {
                                log.writeError("failed to copy icon " + iconPath + " to " + dbPath, e);
                            }
                        }
                    }

                    info.put("serverName", serverName);
                    info.put("updateTime", ClientUtils.convertTimestamp(now));
                    info.put("defaultLanguage", config.getDefaultLanguage());
                    info.put("minPlayTime", config.getMinPlaytime());
                    info.put("showLastOnline", config.isShowLastOnline());
                    info.put("hasIcon", hasIcon);
                    info.put("playersPerPage", config.getPlayersPerPage());
                    info.put("inactiveDays", config.getInactiveDays());
                    info.put("numPlayers", validPlayers.size());
                    info.put("numActive", activePlayers.size());
                    info.put("cacheQ", config.getPlayerCacheUUIDPrefix());

                    final JSONArray infoCrown = new JSONArray(3);
                    infoCrown.put(config.getGoldMedalWeight());
                    infoCrown.put(config.getSilverMedalWeight());
                    infoCrown.put(config.getBronzeMedalWeight());
                    info.put("crown", infoCrown);
                }
                summary.put("info", info);

                // hall of fame
                summary.put("hof", hallOfFameRanking.toJSON());
                hallOfFameRanking.getOrderedEntries().forEach(e -> {
                    summaryRelevantPlayers.add(e.getPlayer());
                });

                // awards
                final JSONObject summaryAwards = new JSONObject(awards.size());
                awards.forEach((id, stat) -> {
                    final JSONObject awardSummary = new JSONObject();
                    awardSummary.put("unit", stat.getUnit().toString());

                    final Ranking<IntValue>.Entry winner = awardWinners.get(stat);
                    if (winner != null) {
                        awardSummary.put("best", winner.toJSON());
                        summaryRelevantPlayers.add(winner.getPlayer());
                    }

                    summaryAwards.put(id, awardSummary);
                });
                summary.put("awards", summaryAwards);

                // events
                final JSONObject summaryEvents = new JSONObject();
                config.getEvents().forEach(event -> {
                    final JSONObject eventSummary = new JSONObject();
                    eventSummary.put("title", event.getTitle());
                    eventSummary.put("startTime", ClientUtils.convertTimestamp(event.getStartTime()));
                    eventSummary.put("endTime", ClientUtils.convertTimestamp(event.getEndTime()));
                    eventSummary.put("link", event.getLinkedStatId());
                    eventSummary.put("active", event.hasStarted(now) && !event.hasEnded(now));

                    final Ranking<IntValue>.Entry winner = eventWinners.get(event);
                    if(winner != null) {
                        eventSummary.put("best", winner.toJSON());
                        summaryRelevantPlayers.add(winner.getPlayer());
                    }

                    summaryEvents.put(event.getId(), eventSummary);
                });
                summary.put("events", summaryEvents);

                // players
                final JSONObject summaryPlayers = new JSONObject();
                summaryRelevantPlayers.forEach(player -> {
                    summaryPlayers.put(player.getUuid(), player.getClientInfo(false));
                });
                summary.put("players", summaryPlayers);

                // write
                final Path summaryPath = dbPath.resolve(DATABASE_SUMMARY);
                FileUtils.writeStringGzipped(summaryPath, summary.toString());
            }
        } catch (Exception e) {
            log.writeError("failed to write database", e);
        }
    }
}
