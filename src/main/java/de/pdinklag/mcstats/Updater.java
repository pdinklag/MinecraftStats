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
import java.util.LinkedList;
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
public class Updater {
    private static final String JSON_FILE_EXT = ".json";
    private static final int MIN_DATA_VERSION = 1451; // 17w47a
    private static final String DATABASE_PLAYERS_JSON = "players.json";
    private static final String DATABASE_RANKINGS = "rankings";
    private static final String DATABASE_PLAYERCACHE = "playercache";
    private static final String DATABASE_PLAYERDATA = "playerdata";
    private static final String DATABASE_PLAYERLIST = "playerlist";
    private static final String DATABASE_PLAYERLIST_ALL_FORMAT = "all%d.json.gz";
    private static final String DATABASE_PLAYERLIST_ACTIVE_FORMAT = "active%d.json.gz";
    private static final String DATABASE_SUMMARY = "summary.json.gz";

    private static final int TICKS_PER_SECOND = 20;
    private static final int MINUTES_TO_TICKS = 60 * TICKS_PER_SECOND;

    private static final long DAYS_TO_MILLISECONDS = 24L * 60L * 60L * 1000L;

    // initialization
    private final Config config;
    private final LogWriter log;

    protected final LinkedList<PlayerFilter> playerFilters = new LinkedList<>();
    private final ArrayList<Stat> awards = new ArrayList<>();

    protected final LinkedList<PlayerProfileProvider> localProfileProviders = new LinkedList<>();
    private final PlayerProfileProvider authenticProfileProvider;

    // paths
    private final Path dbPath;
    private final Path dbPlayersJsonPath;
    private final Path dbRankingsPath;
    private final Path dbPlayercachePath;
    private final Path dbPlayerdataPath;
    private final Path dbPlayerlistPath;

    private HashMap<String, Player> processPlayers() {
        HashMap<String, Player> discoveredPlayers = new HashMap<>();

        // discover players in data sources
        config.getDataSources().forEach(source -> {
            Path statsPath = source.getPlayerStatsPath();
            try {
                Files.list(statsPath).forEach(path -> {
                    try {
                        final String filename = path.getFileName().toString();
                        if (Files.isRegularFile(path) && filename.endsWith(JSON_FILE_EXT)) {
                            // extract UUID from filename
                            final String uuid = filename.substring(0, filename.length() - JSON_FILE_EXT.length());

                            // read JSON
                            final JSONObject json = new JSONObject(Files.readString(path));
                            final JSONObject stats = json.getJSONObject("stats");

                            // TODO: advancements

                            // gather basic information
                            Player player = discoveredPlayers.getOrDefault(uuid, new Player(uuid));

                            final long lastOnlineTime = Files.getLastModifiedTime(path).toMillis();
                            player.setLastOnlineTime(Math.max(player.getLastOnlineTime(), lastOnlineTime));

                            final int dataVersion = DefaultReaders.DATA_VERSION_READER.read(json).toInt();
                            player.setDataVersion(Math.max(player.getDataVersion(), dataVersion));

                            final int playTime = DefaultReaders.PLAYTIME_READER.read(stats).toInt();
                            player.setPlaytime(Math.max(player.getPlaytime(), playTime));

                            // gather stats
                            player.getStats().gather(awards, stats, dataVersion);

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
        return discoveredPlayers;
    }

    private boolean filterPlayer(Player player) {
        for (PlayerFilter filter : playerFilters) {
            if (!filter.filter(player)) {
                return false;
            }
        }
        return true;
    }

    protected PlayerProfileProvider createAuthenticProfileProvider() {
        return new MojangAPIPlayerProfileProvider();
    }

    private void writePlayerList(Collection<Player> players, String filenameFormat) {
        final ArrayList<Player> playersSorted = new ArrayList<>(players);
        Collections.sort(playersSorted, (a, b) -> a.getProfile().getName().compareTo(b.getProfile().getName()));

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
        this.dbRankingsPath = dbPath.resolve(DATABASE_RANKINGS);
        this.dbPlayercachePath = dbPath.resolve(DATABASE_PLAYERCACHE);
        this.dbPlayerdataPath = dbPath.resolve(DATABASE_PLAYERDATA);
        this.dbPlayerlistPath = dbPath.resolve(DATABASE_PLAYERLIST);

        // create local providers
        // players.json
        if (Files.isRegularFile(dbPlayersJsonPath)) {
            try {
                JSONObject playersJson = new JSONObject(Files.readString(dbPlayersJsonPath));
                localProfileProviders.add(new DatabasePlayerProfileProvider(playersJson));
            } catch (Exception e) {
                log.writeError("failed to load players from previous database: " + dbPlayersJsonPath.toString(), e);
            }
        }

        // usercache.json
        config.getDataSources().forEach(source -> {
            Path usercachePath = MinecraftServerUtils.getUserCachePath(source.getServerPath());
            if (Files.isRegularFile(usercachePath)) {
                try {
                    JSONArray usercacheJson = new JSONArray(Files.readString(usercachePath));
                    localProfileProviders.add(new UserCachePlayerProfileProvider(usercacheJson));
                } catch (Exception e) {
                    log.writeError("failed to read usercache: " + usercachePath.toString(), e);
                }
            }
        });

        // create authentic provider
        authenticProfileProvider = createAuthenticProfileProvider();

        // filter players whose data version is too low
        playerFilters.add(new DataVersionPlayerFilter(MIN_DATA_VERSION, Integer.MAX_VALUE));

        // filter players who didn't play long enough
        playerFilters.add(new MinPlaytimePlayerFilter(MINUTES_TO_TICKS * config.getMinPlaytime()));

        // filter players who are inactive
        playerFilters.add(new LastOnlinePlayerFilter(
                System.currentTimeMillis() - DAYS_TO_MILLISECONDS * (long) config.getInactiveDays()));

        // exclude banned players
        if (config.isExcludeBanned()) {
            config.getDataSources().forEach(source -> {
                Path bannedPlayersPath = MinecraftServerUtils.getBannedPlayersPath(source.getServerPath());
                if (Files.isRegularFile(bannedPlayersPath)) {
                    try {
                        JSONArray ops = new JSONArray(Files.readString(bannedPlayersPath));
                        playerFilters.add(new JSONPlayerFilter(ops));
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
                        playerFilters.add(new JSONPlayerFilter(ops));
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
            playerFilters.add(filter);
        }

        // discover and instantiate stats
        try {
            ResourceUtils.getResourceFilenames(getClass().getClassLoader(), "stats").forEach(resource -> {
                try {
                    final JSONObject obj = new JSONObject(
                            StreamUtils.readStreamFully(getClass().getResourceAsStream(resource)));
                    awards.add(StatParser.parse(obj));
                } catch (Exception e2) {
                    log.writeError("failed to load stat from resources: " + resource, e2);
                }
            });
        } catch (Exception e) {
            log.writeError("failed to discover stats", e);
        }
    }

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
        HashMap<String, Player> allPlayers = processPlayers();

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
        HashMap<String, Player> activePlayers = new HashMap<>();
        ArrayList<Player> validPlayers = new ArrayList<>();
        allPlayers.forEach((uuid, player) -> {
            // use local sources
            for (PlayerProfileProvider provider : localProfileProviders) {
                player.setProfile(provider.getPlayerProfile(player));
                if (player.getProfile().hasName()) {
                    break;
                }
            }

            // filter active players
            final boolean isActive = filterPlayer(player);
            if (isActive) {
                activePlayers.put(uuid, player);
            }

            // use authentic sources if due
            if (isActive || config.isUpdateInactive()) {
                final long updateInterval = DAYS_TO_MILLISECONDS * (long) config.getProfileUpdateInterval();
                final long timeSinceUpdate = now - player.getProfile().getLastUpdateTime();
                if (timeSinceUpdate >= updateInterval) {
                    log.writeLine("updating profile for " + player.getUuid() + " ...");
                    player.setProfile(authenticProfileProvider.getPlayerProfile(player));
                }
            }

            // filter valid players
            if (player.getProfile().hasName()) {
                validPlayers.add(player);
            }
        });

        // write database
        try {
            // create directories
            Files.createDirectories(dbRankingsPath);
            Files.createDirectories(dbPlayercachePath);
            Files.createDirectories(dbPlayerdataPath);
            Files.createDirectories(dbPlayerlistPath);

            // compute and write rankings
            HashMap<Stat, Ranking<IntValue>.Entry> best = new HashMap<>();
            awards.forEach(award -> {
                if (award.isVersionSupported(serverDataVersion)) {
                    // rank players
                    final Ranking<IntValue> ranking = new Ranking<IntValue>(activePlayers.values(), player -> {
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
                        best.put(award, rankingEntries.get(0));
                    }

                    // write award summary file
                    Path awardJsonPath = dbRankingsPath.resolve(award.getId() + JSON_FILE_EXT);
                    try {
                        Files.writeString(awardJsonPath, ranking.toJSON().toString());
                    } catch (Exception e) {
                        log.writeError("failed to write award data: " + awardJsonPath, e);
                    }
                } else {
                    log.writeLine("award " + award.getId() + " is not supported by server (data version "
                            + serverDataVersion + ")");
                }
            });

            // write playerdata
            activePlayers.forEach((uuid, player) -> {
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
            writePlayerList(activePlayers.values(), DATABASE_PLAYERLIST_ACTIVE_FORMAT);

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
                hallOfFameRanking = new Ranking<CrownScoreValue>(activePlayers.values(), player -> {
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
                        for (DataSource dataSource : config.getDataSources()) {
                            serverName = MinecraftServerUtils.getMOTD(dataSource.getServerPath());
                            if (serverName != null) {
                                serverName = serverName.replace("\\n", "<br>");
                                break;
                            }
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
                awards.forEach(stat -> {
                    final JSONObject awardSummary = new JSONObject();
                    awardSummary.put("unit", stat.getUnit().toString());

                    final Ranking<IntValue>.Entry awardBest = best.get(stat);
                    if (awardBest != null) {
                        awardSummary.put("best", awardBest.toJSON());
                        summaryRelevantPlayers.add(awardBest.getPlayer());
                    }

                    summaryAwards.put(stat.getId(), awardSummary);
                });
                summary.put("awards", summaryAwards);

                // events
                summary.put("events", new JSONObject()); // TODO: fill event data

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
