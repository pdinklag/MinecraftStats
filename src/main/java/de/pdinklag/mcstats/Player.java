package de.pdinklag.mcstats;

/**
 * Represents a player on the Minecraft server.
 */
public class Player {
    private final String uuid;

    private PlayerProfile profile;

    /**
     * Constructs a new player object.
     * @param uuid the player's UUID.
     */
    public Player(String uuid) {
        this.uuid = uuid;
    }

    /**
     * Gets the player's UUID.
     * @return the player's UUID
     */
    public String getUuid() {
        return uuid;
    }

    /**
     * Gets the player's known profile, if any.
     * @return the player's known profile, or null if none is known
     */
    public PlayerProfile getProfile() {
        return profile;
    }

    /**
     * Sets the player's known profile.
     * @param profile the known profile
     */
    public void setProfile(PlayerProfile profile) {
        this.profile = profile;
    }
}
