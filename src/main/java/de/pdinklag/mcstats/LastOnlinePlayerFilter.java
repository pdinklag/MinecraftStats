package de.pdinklag.mcstats;

/**
 * Filters players according to their last online time.
 */
public class LastOnlinePlayerFilter implements PlayerFilter {
    private final long latestOnlineTime;

    /**
     * Constructs a last online filter.
     * @param latestOnlineTime the latest allowed online time
     */
    public LastOnlinePlayerFilter(long latestOnlineTime) {
        this.latestOnlineTime = latestOnlineTime;
    }

    @Override
    public boolean filter(Player player) {
        return player.getLastOnlineTime() >= latestOnlineTime;
    }
    
}
