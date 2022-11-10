package de.pdinklag.mcstats;

/**
 * Filters players according to their play time.
 */
public class MinPlaytimePlayerFilter implements PlayerFilter {
    private final int minPlaytime;

    /**
     * Constructs a playtime filter.
     * @param minPlaytime the minimum playtime in ticks
     */
    public MinPlaytimePlayerFilter(int minPlaytime) {
        this.minPlaytime = minPlaytime;
    }

    @Override
    public boolean filter(Player player) {
        return player.getPlaytime() >= minPlaytime;
    }
    
}
