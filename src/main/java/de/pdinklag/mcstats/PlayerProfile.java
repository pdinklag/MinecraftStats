package de.pdinklag.mcstats;

public class PlayerProfile {
    private final String name;
    private final String skin;
    private final long lastUpdateTime;

    public PlayerProfile(String name, String skin, long lastUpdateTime) {
        this.name = name;
        this.skin = skin;
        this.lastUpdateTime = lastUpdateTime;
    }

    public String getName() {
        return name;
    }

    public String getSkin() {
        return skin;
    }

    public long getLastUpdateTime() {
        return lastUpdateTime;
    }
}
