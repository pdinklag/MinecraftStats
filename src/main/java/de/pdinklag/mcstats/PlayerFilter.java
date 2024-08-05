package de.pdinklag.mcstats;

/**
 * Interface for player filters.
 */
public interface PlayerFilter {
    /**
     * Tests whether a player should be filtered, i.e., included in the database.
     * @param player the player in question
     * @return true if the player stays, false if it goes
     */
    public boolean filter(Player player);

    /**
     * Returns a string describing the filter criteria of this filter.
     * @return a string describing the filter criteria of this filter
     */
    public String getFilterCriteria();
}
