package de.pdinklag.mcstats;

/**
 * Contains profile information for a player.
 */
public class PlayerProfile {
    private final String name;
    private final String skin;

    /**
     * Constructs profile information.
     * @param name the player's name
     * @param skin the identifier (URL suffix) of the player's skin
     */
    public PlayerProfile(String name, String skin) {
        this.name = name;
        this.skin = skin;
    }

    /**
     * Gets the player's name.
     * @return the player's name
     */
    public String getName() {
        return name;
    }

    /**
     * Gets the player's skin identifier.
     * @return the player's skin identifier
     */
    public String getSkin() {
        return skin;
    }
}
