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
    private final String worldName;

    /**
     * Constructs a data source.
     * @param serverPath
     * @param worldName
     */
    public FileSystemDataSource(Path serverPath, String worldName) {
        this.serverPath = serverPath;
        this.worldName = worldName;
    }

    @Override
    public Path getServerPath() {
        return serverPath;
    }

    /**
     * Gets the directory that contains the per-player directories (stats, advancements).
     * Older versions keep them directly in the world directory; newer versions
     * (confirmed for Minecraft 26.2, data version 4903) group them in a "players" subdirectory.
     * @return the directory containing the per-player directories
     */
    private Path getPlayersPath() {
        final Path worldPath = serverPath.resolve(worldName);
        final Path playersPath = worldPath.resolve(PLAYERS_PATH_NAME);
        return Files.isDirectory(playersPath.resolve(STATS_PATH_NAME)) ? playersPath : worldPath;
    }

    @Override
    public Path getPlayerStatsPath() {
        return getPlayersPath().resolve(STATS_PATH_NAME);
    }

    @Override
    public Path getPlayerAdvancementsPath() {
        return getPlayersPath().resolve(ADVANCEMENTS_PATH_NAME);
    }
}
