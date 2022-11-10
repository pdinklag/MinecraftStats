package de.pdinklag.mcstats;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.LinkedList;

import org.json.JSONArray;
import org.json.JSONObject;

import de.pdinklag.mcstats.util.MinecraftServerUtils;

/**
 * The heart of MinecraftStats.
 */
public abstract class Updater {
    private static final String JSON_FILE_EXT = ".json";
    private static final int MIN_DATA_VERSION = 1451; // 17w47a
    private static final String DATABASE_PLAYERS_JSON = "players.json";

    // initialization
    private final Path databasePath;
    private final LinkedList<DataSource> dataSources = new LinkedList<>();

    protected final LinkedList<PlayerFilter> playerFilters = new LinkedList<>();
    private final ArrayList<Stat> awards = new ArrayList<>();

    protected final LinkedList<PlayerProfileProvider> localProfileProviders = new LinkedList<>();
    private final PlayerProfileProvider authenticProfileProvider;

    // config
    protected long profileUpdateInterval = 0;

    private HashMap<String, Player> processPlayers() {
        HashMap<String, Player> discoveredPlayers = new HashMap<>();

        // discover players in data sources
        dataSources.forEach(source -> {
            Path statsPath = source.getPlayerStatsPath();
            try {
                Files.list(statsPath).forEach(path -> {
                    try {
                        if (Files.isRegularFile(path) && path.endsWith(JSON_FILE_EXT)) {
                            // extract UUID from filename
                            final String filename = path.getFileName().toString();
                            final String uuid = filename.substring(0, filename.length() - JSON_FILE_EXT.length());

                            // read JSON
                            final JSONObject stats = new JSONObject(Files.readString(path));

                            // gather basic information
                            Player player = discoveredPlayers.getOrDefault(uuid, new Player(uuid));

                            final long lastOnlineTime = Files.getLastModifiedTime(path).toMillis();
                            player.setLastOnlineTime(Math.max(player.getLastOnlineTime(), lastOnlineTime));

                            final int dataVersion = DefaultReaders.DATA_VERSION_READER.read(stats).toInt();
                            player.setDataVersion(Math.max(player.getDataVersion(), dataVersion));

                            final int playTime = DefaultReaders.PLAYTIME_READER.read(stats).toInt();
                            player.setPlaytime(Math.max(player.getPlaytime(), playTime));

                            // gather stats
                            player.getStats().gather(awards, stats);

                            // register in set of players
                            discoveredPlayers.put(uuid, player);
                        }
                    } catch (Exception e) {
                        System.err.println("failed to process file: " + path.toString());
                        e.printStackTrace();
                    }
                });
            } catch (IOException e) {
                System.err.println("failed to run discovery on data source: " + statsPath.toString());
                e.printStackTrace();
            }
        });
        return discoveredPlayers;
    }

    private boolean filterPlayer(Player player) {
        for (PlayerFilter filter : playerFilters) {
            if (!filter.filter(player))
                return false;
        }
        return true;
    }

    protected PlayerProfileProvider createAuthenticProfileProvider() {
        return new MojangAPIPlayerProfileProvider();
    }

    protected Updater(Path databasePath, Collection<DataSource> sources) {
        this.databasePath = databasePath;
        dataSources.addAll(sources);

        // create local providers
        {
            // players.json
            Path playersJsonPath = databasePath.resolve(DATABASE_PLAYERS_JSON);
            if (Files.isRegularFile(playersJsonPath)) {
                try {
                    JSONObject playersJson = new JSONObject(Files.readString(playersJsonPath));
                    localProfileProviders.add(new DatabasePlayerProfileProvider(playersJson));
                } catch (Exception e) {
                    System.err.println("failed to load players from previous database: " + playersJsonPath.toString());
                    e.printStackTrace();
                }
            }
        }

        // usercache.json
        dataSources.forEach(source -> {
            Path usercachePath = MinecraftServerUtils.getUserCachePath(source.getServerPath());
            if (Files.isRegularFile(usercachePath)) {
                try {
                    JSONArray usercacheJson = new JSONArray(Files.readString(usercachePath));
                    localProfileProviders.add(new UserCachePlayerProfileProvider(usercacheJson));
                } catch (Exception e) {
                    System.err.println("failed to read usercache: " + usercachePath.toString());
                    e.printStackTrace();
                }
            }
        });

        // create authentic provider
        authenticProfileProvider = createAuthenticProfileProvider();

        // TODO: parse and instantiate stats

        // filter players whose data version is too low
        playerFilters.add(new DataVersionPlayerFilter(MIN_DATA_VERSION, Integer.MAX_VALUE));

        // TODO: add MinPlaytimePlayerFilter
        // TODO: add LastOnlinePlayerFilter
    }

    public void run() {
        // get current timestamp
        final long now = System.currentTimeMillis();

        // get players
        HashMap<String, Player> players = new HashMap<>();
        {
            // discover and process players
            HashMap<String, Player> discoveredPlayers = processPlayers();

            // filter players
            discoveredPlayers.forEach((uuid, player) -> {
                if (filterPlayer(player)) {
                    // keep player
                    players.put(uuid, player);
                }
            });
        }

        // get player profiles
        players.forEach((uuid, player) -> {
            // use local sources
            for (PlayerProfileProvider provider : localProfileProviders) {
                player.setProfile(provider.getPlayerProfile(player));
                if (player.getProfile().hasName()) {
                    break;
                }
            }

            // use authentic sources if due
            if (now - player.getProfile().getLastUpdateTime() >= profileUpdateInterval) {
                player.setProfile(authenticProfileProvider.getPlayerProfile(player));
            }
        });

        // TODO: compute rankings
        // TODO: process crown score
        // TODO: write database for client
    }
}
