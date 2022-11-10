package de.pdinklag.mcstats;

/**
 * Represents a player tracked by MinecraftStats.
 */
public class Player {
    // identifier
    private final String uuid;

    // discovery and filtering information
    private long lastOnlineTime = 0;
    private int playtime = 0;
    private int dataVersion = 0;

    // update information
    private PlayerProfile profile;
    private final PlayerStats stats = new PlayerStats();

    /**
     * Constructs a new player object.
     * @param uuid the player's UUID
     */
    public Player(String uuid) {
        this.uuid = uuid;
        this.profile = new PlayerProfile(uuid, null);
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

    public PlayerStats getStats() {
        return stats;
    }

    public long getLastOnlineTime() {
        return lastOnlineTime;
    }

    public void setLastOnlineTime(long lastOnlineTime) {
        this.lastOnlineTime = lastOnlineTime;
    }

    public int getDataVersion() {
        return dataVersion;
    }

    public void setDataVersion(int dataVersion) {
        this.dataVersion = dataVersion;
    }

    public int getPlaytime() {
        return playtime;
    }

    public void setPlaytime(int playtime) {
        this.playtime = playtime;
    }
}
