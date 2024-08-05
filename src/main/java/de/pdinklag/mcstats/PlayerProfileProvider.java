package de.pdinklag.mcstats;

/**
 * Interface for objects that provide player profiles.
 */
public interface PlayerProfileProvider {
    /**
     * Attempts to provide a profile for the given player.
     * @param player the player in question
     * @return a profile for the player, or null if none can be provided
     */
    public PlayerProfile getPlayerProfile(Player player);

    public String getDisplayString();
}
