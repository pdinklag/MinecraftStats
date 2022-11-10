package de.pdinklag.mcstats;

import java.nio.file.Path;

/**
 * Describes a MinecraftStats data source on the local file system.
 */
public class FileSystemDataSource implements DataSource {
    private static final String STATS_PATH_NAME = "stats";

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

    @Override
    public Path getPlayerStatsPath() {
        return serverPath.resolve(worldName).resolve(STATS_PATH_NAME);
    }
}
