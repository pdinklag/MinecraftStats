package de.pdinklag.mcstats;

/**
 * Contains profile information for a player.
 */
public class PlayerProfile {
    private final String name;
    private final String skin;
    private final long lastUpdateTime;

    /**
     * Constructs profile information.
     * 
     * @param name           the player's name
     * @param skin           the identifier (URL suffix) of the player's skin
     * @param lastUpdateTime the last time that the profile was updated using an
     *                       authentic source
     */
    public PlayerProfile(String name, String skin, long lastUpdateTime) {
        this.name = (name != null) ? name : "";
        this.skin = skin;
        this.lastUpdateTime = lastUpdateTime;
    }

    /**
     * Constructs unvalidated profile information.
     * 
     * @param name the player's name
     */
    public PlayerProfile(String name) {
        this(name, null, 0);
    }

    /**
     * Constructs empty profile information.
     */
    public PlayerProfile() {
        this("", null, 0);
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
}
