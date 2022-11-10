package de.pdinklag.mcstats;

/**
 * Filters players according to their data version.
 */
public class DataVersionPlayerFilter implements PlayerFilter {
    private final int minVersion;
    private final int maxVersion;

    /**
     * Constructs a data version filter.
     * @param minVersion
     * @param maxVersion
     */
    public DataVersionPlayerFilter(int minVersion, int maxVersion) {
        this.minVersion = minVersion;
        this.maxVersion = maxVersion;
    }

    @Override
    public boolean filter(Player player) {
        int dataVersion = player.getDataVersion();
        return dataVersion >= minVersion && dataVersion <= maxVersion;
    }
    
}
