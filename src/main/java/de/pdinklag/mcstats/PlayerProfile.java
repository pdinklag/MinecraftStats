package de.pdinklag.mcstats;

public class PlayerProfile {
    private final String name;
    private final String skin;

    public PlayerProfile(String name, String skin) {
        this.name = name;
        this.skin = skin;
    }

    public String getName() {
        return name;
    }

    public String getSkin() {
        return skin;
    }
}
