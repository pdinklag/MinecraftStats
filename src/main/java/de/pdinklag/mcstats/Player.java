package de.pdinklag.mcstats;

import org.json.JSONObject;

import de.pdinklag.mcstats.util.ClientUtils;

/**
 * Represents a player tracked by MinecraftStats.
 */
public class Player {
    private static class DummyProfileProvider implements PlayerProfileProvider {
        @Override
        public PlayerProfile getPlayerProfile(Player player) {
            return new PlayerProfile(this);
        }

        @Override
        public String getDisplayString() {
            return "initialization";
        }
    }

    private static final DummyProfileProvider dummyProfileProvider = new DummyProfileProvider();

    // identifier
    private final String uuid;
    private AccountType accountType;

    // discovery and filtering information
    private long lastOnlineTime = 0;
    private int playtime = 0;
    private int dataVersion = 0;

    // update information
    private PlayerProfile profile = dummyProfileProvider.getPlayerProfile(this);
    private final PlayerStats stats = new PlayerStats();

    /**
     * Constructs a new player object.
     * 
     * @param uuid the player's UUID
     */
    public Player(String uuid) {
        this.uuid = uuid;
        this.accountType = AccountType.detect(uuid);
    }

    /**
     * Gets the player's UUID.
     * 
     * @return the player's UUID
     */
    public String getUuid() {
        return uuid;
    }

    /**
     * Gets the player's account type.
     * 
     * @return the player's account type.
     */
    public AccountType getAccountType() {
        return accountType;
    }

    /**
     * Sets the player's account type.
     * 
     * @param accountType the player's account type.
     */
    public void setAccountType(AccountType accountType) {
        this.accountType = accountType;
    }

    /**
     * Gets the player's known profile, if any.
     * 
     * @return the player's known profile, or null if none is known
     */
    public PlayerProfile getProfile() {
        return profile;
    }

    /**
     * Sets the player's known profile.
     * 
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

    public JSONObject getClientInfo(boolean includeUuid) {
        JSONObject info = new JSONObject();
        if (includeUuid) {
            info.put("uuid", uuid);
        }

        info.put("name", getProfile().getName());

        String skin = getProfile().getSkin();
        if (skin != null) {
            info.put("skin", skin);
        } else {
            info.put("skin", false);
        }

        info.put("last", ClientUtils.convertTimestamp(lastOnlineTime));
        return info;
    }

    public String getDisplayString() {
        if (getProfile().hasName()) {
            return uuid + " (" + profile.getName() + ")";
        } else {
            return uuid + " (name N/A)";
        }
    }
}
