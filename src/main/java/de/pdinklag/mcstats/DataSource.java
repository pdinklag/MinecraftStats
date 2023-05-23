package de.pdinklag.mcstats;

import java.nio.file.Path;

/**
 * Interface for MinecraftStats data sources.
 */
public interface DataSource {
    public Path getServerPath();
    
    public Path getPlayerStatsPath();

    public Path getPlayerAdvancementsPath();
}
