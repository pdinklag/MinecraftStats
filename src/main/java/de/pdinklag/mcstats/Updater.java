package de.pdinklag.mcstats;

import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.nio.file.Files;
import java.nio.file.OpenOption;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Formatter;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.zip.GZIPOutputStream;

import org.bukkit.util.FileUtil;
import org.json.JSONArray;
import org.json.JSONObject;

import de.pdinklag.mcstats.util.ResourceUtils;
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
    private static final String DATABASE_PLAYERDATA = "playerdata";
    private static final String DATABASE_PLAYERLIST = "playerlist";
    private static final String DATABASE_PLAYERLIST_ALL_FORMAT = "all%d.json.gz";
    private static final String DATABASE_PLAYERLIST_ACTIVE_FORMAT = "active%d.json.gz";

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

        final int playersPerPage = config.getPlayersPePage();
        final int numPlayers = players.size();
        final int numPages = (int) Math.ceil((double) numPlayers / playersPerPage);

        for (int pageNum = 0; pageNum < numPages; pageNum++) {
            final int first = pageNum * playersPerPage;
            final int last = Math.min(first + playersPerPage, numPlayers);

            final JSONArray page = new JSONArray(playersPerPage);
            for (var i = first; i < last; i++) {
                page.put(playersSorted.get(i).getClientInfo());
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

        // update player profiles
        HashMap<String, Player> activePlayers = new HashMap<>();
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
        });

        // write database
        try {
            // create directories
            Files.createDirectories(dbRankingsPath);
            Files.createDirectories(dbPlayerdataPath);
            Files.createDirectories(dbPlayerlistPath);

            // compute and write rankings
            HashMap<Stat, Ranking.Entry> best = new HashMap<>();
            awards.forEach(award -> {
                if (award.isVersionSupported(serverDataVersion)) {
                    // rank players
                    final Ranking ranking = new Ranking(activePlayers.values(), player -> {
                        return player.getStats().get(award);
                    });

                    // notify players of their rankings
                    List<Ranking.Entry> rankingEntries = ranking.getOrderedEntries();
                    for (int rank = 0; rank < rankingEntries.size(); rank++) {
                        Ranking.Entry e = rankingEntries.get(rank);
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

            // write playerlist
            writePlayerList(allPlayers.values(), DATABASE_PLAYERLIST_ALL_FORMAT);
            writePlayerList(activePlayers.values(), DATABASE_PLAYERLIST_ACTIVE_FORMAT);

            // write players.json for next update
            Files.writeString(dbPlayersJsonPath,
                    DatabasePlayerProfileProvider.createDatabase(allPlayers.values()).toString());

            // crown ranking for Hall of Fame
            final Ranking hallOfFameRanking;
            {
                final int goldWeight = config.getGoldMedalWeight();
                final int silverWeight = config.getSilverMedalWeight();
                final int bronzeWeight = config.getBronzeMedalWeight();
                hallOfFameRanking = new Ranking(activePlayers.values(), player -> {
                    return new IntValue(player.getStats().getCrownScore(goldWeight, silverWeight, bronzeWeight));
                });
            }

            // TODO: write summary

        } catch (Exception e) {
            log.writeError("failed to write database", e);
        }

        // TODO: write database for client
    }
}
