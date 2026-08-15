package de.pdinklag.mcstats;

import java.nio.file.Files;
import java.nio.file.Path;

/**
 * Describes a MinecraftStats data source on the local file system.
 */
public class FileSystemDataSource implements DataSource {
    private static final String ADVANCEMENTS_PATH_NAME = "advancements";
    private static final String STATS_PATH_NAME = "stats";
    private static final String PLAYERS_PATH_NAME = "players";

    private final Path serverPath;
    private final Path worldPath;

    /**
     * Constructs a data source for a world located in the server directory.
     * @param serverPath the server directory
     * @param worldName the name of the world directory within the server directory
     */
    public FileSystemDataSource(Path serverPath, String worldName) {
        this(serverPath, serverPath.resolve(worldName));
    }

    /**
     * Constructs a data source for a world at an arbitrary location.
     * The server path is kept separate, because the server files (user cache, banned players, ops and icon)
     * are read relative to it no matter where the world itself is stored.
     * @param serverPath the server directory
     * @param worldPath the world directory containing the player stats and advancements
     */
    public FileSystemDataSource(Path serverPath, Path worldPath) {
        this.serverPath = serverPath;
        this.worldPath = worldPath;
    }

    @Override
    public Path getServerPath() {
        return serverPath;
    }

    /**
     * Gets the directory that contains the player data directories.
     * Newer Minecraft versions store the player data in a "players" subdirectory of the world,
     * while older versions store it directly in the world directory.
     * Both layouts are supported, so that the same configuration works before and after a server update.
     * @return the directory containing the player stats and advancements directories
     */
    private Path getPlayerDataPath() {
        final Path playersPath = worldPath.resolve(PLAYERS_PATH_NAME);
        if (Files.isDirectory(playersPath.resolve(STATS_PATH_NAME))) {
            return playersPath;
        } else {
            return worldPath;
        }
    }

    @Override
    public Path getPlayerStatsPath() {
        return getPlayerDataPath().resolve(STATS_PATH_NAME);
    }

    @Override
    public Path getPlayerAdvancementsPath() {
        return getPlayerDataPath().resolve(ADVANCEMENTS_PATH_NAME);
    }
}
