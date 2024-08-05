package de.pdinklag.mcstats;

/**
 * Contains profile information for a player.
 */
public class PlayerProfile {
    private final String name;
    private final String skin;
    private final long lastUpdateTime;
    private final PlayerProfileProvider provider;

    /**
     * Constructs profile information.
     * 
     * @param name           the player's name
     * @param skin           the identifier (URL suffix) of the player's skin
     * @param lastUpdateTime the last time that the profile was updated using an
     *                       authentic source
     * @param provider       the provider of this profile
     */
    public PlayerProfile(String name, String skin, long lastUpdateTime, PlayerProfileProvider provider) {
        this.name = (name != null) ? name : "";
        this.skin = skin;
        this.lastUpdateTime = lastUpdateTime;
        this.provider = provider;
    }

    /**
     * Constructs unvalidated profile information.
     * 
     * @param name the player's name
     */
    public PlayerProfile(String name, PlayerProfileProvider provider) {
        this(name, null, 0, provider);
    }

    /**
     * Constructs empty profile information.
     */
    public PlayerProfile(PlayerProfileProvider provider) {
        this("", null, 0, provider);
    }

    /**
     * Tests whether the profile has a player name.
     * 
     * @return true if it has a name, false otherwise
     */
    public boolean hasName() {
        return !name.isEmpty();
    }

    /**
     * Gets the player's name.
     * 
     * @return the player's name
     */
    public String getName() {
        return name;
    }

    /**
     * Gets the player's skin identifier.
     * 
     * @return the player's skin identifier
     */
    public String getSkin() {
        return skin;
    }

    /**
     * Reports the last time that the profile was updated using an authentic
     * source.
     * 
     * @return the last update time of the profile
     */
    public long getLastUpdateTime() {
        return lastUpdateTime;
    }

    /**
     * Gets the provider of this profile.
     * 
     * @return the provider of this profile
     */
    public PlayerProfileProvider getProvider() {
        return provider;
    }
}
