package de.pdinklag.mcstats;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONObject;

import de.pdinklag.mcstats.util.ResourceUtils;
import de.pdinklag.mcstats.util.MinecraftServerUtils;
import de.pdinklag.mcstats.util.StreamUtils;

/**
 * The heart of MinecraftStats.
 */
public class Updater {
    private static final String JSON_FILE_EXT = ".json";
    private static final int MIN_DATA_VERSION = 1451; // 17w47a
    private static final String DATABASE_PLAYERS_JSON = "players.json";

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
    private final Path playersJsonPath;

    private HashMap<String, Player> discoverPlayers() {
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
                            player.getStats().gather(awards, stats);

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

    public Updater(Config config, LogWriter log) {
        this.config = config;
        this.log = log;

        // cache some paths
        this.dbPath = config.getDatabasePath();
        this.playersJsonPath = dbPath.resolve(DATABASE_PLAYERS_JSON);

        // create local providers
        // players.json
        if (Files.isRegularFile(playersJsonPath)) {
            try {
                JSONObject playersJson = new JSONObject(Files.readString(playersJsonPath));
                localProfileProviders.add(new DatabasePlayerProfileProvider(playersJson));
            } catch (Exception e) {
                log.writeError("failed to load players from previous database: " + playersJsonPath.toString(), e);
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
        HashMap<String, Player> allPlayers = discoverPlayers();
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

        // compute rankings
        awards.forEach(award -> {
            final Ranking ranking = new Ranking(activePlayers.values(), player -> {
                return player.getStats().get(award);
            });

            final List<Ranking.Entry> orderedEntries = ranking.getOrderedEntries();
            log.writeLine("best player for award " + award.getId() + " is " +
                    (orderedEntries.isEmpty() ? "nobody" : orderedEntries.get(0).getPlayer().getProfile().getName() + " with score " + orderedEntries.get(0).getScore()));
        });

        // TODO: process crown score

        // write players.json
        try {
            JSONObject db = DatabasePlayerProfileProvider.createDatabase(allPlayers.values());
            Files.writeString(playersJsonPath, db.toString(4));
        } catch (Exception e) {
            log.writeError("failed to write players database: " + playersJsonPath.toString(), e);
        }

        // TODO: write database for client
    }
}
