package de.pdinklag.mcstats;

import java.nio.file.Files;
import java.nio.file.Path;

/**
 * Describes a MinecraftStats data source on the local file system.
 */
public class FileSystemDataSource implements DataSource {
    private static final String ADVANCEMENTS_PATH_NAME = "advancements";
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
        if (worldName != null && !worldName.isEmpty()) {
            Path playersStatsWorld = serverPath.resolve(worldName).resolve("players").resolve(STATS_PATH_NAME);
            if (Files.isDirectory(playersStatsWorld)) {
                return playersStatsWorld;
            }
            Path pathWithWorld = serverPath.resolve(worldName).resolve(STATS_PATH_NAME);
            if (Files.isDirectory(pathWithWorld)) {
                return pathWithWorld;
            }
        }
        Path playersStatsDirect = serverPath.resolve("players").resolve(STATS_PATH_NAME);
        if (Files.isDirectory(playersStatsDirect)) {
            return playersStatsDirect;
        }
        Path pathDirect = serverPath.resolve(STATS_PATH_NAME);
        if (Files.isDirectory(pathDirect)) {
            return pathDirect;
        }
        return (worldName != null && !worldName.isEmpty())
                ? serverPath.resolve(worldName).resolve("players").resolve(STATS_PATH_NAME)
                : pathDirect;
    }

    @Override
    public Path getPlayerAdvancementsPath() {
        if (worldName != null && !worldName.isEmpty()) {
            Path playersAdvancementsWorld = serverPath.resolve(worldName).resolve("players").resolve(ADVANCEMENTS_PATH_NAME);
            if (Files.isDirectory(playersAdvancementsWorld)) {
                return playersAdvancementsWorld;
            }
            Path pathWithWorld = serverPath.resolve(worldName).resolve(ADVANCEMENTS_PATH_NAME);
            if (Files.isDirectory(pathWithWorld)) {
                return pathWithWorld;
            }
        }
        Path playersAdvancementsDirect = serverPath.resolve("players").resolve(ADVANCEMENTS_PATH_NAME);
        if (Files.isDirectory(playersAdvancementsDirect)) {
            return playersAdvancementsDirect;
        }
        Path pathDirect = serverPath.resolve(ADVANCEMENTS_PATH_NAME);
        if (Files.isDirectory(pathDirect)) {
            return pathDirect;
        }
        return (worldName != null && !worldName.isEmpty())
                ? serverPath.resolve(worldName).resolve("players").resolve(ADVANCEMENTS_PATH_NAME)
                : pathDirect;
    }
}

