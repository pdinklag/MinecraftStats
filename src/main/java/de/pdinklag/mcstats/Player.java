package de.pdinklag.mcstats;

public class Player {
    private final String uuid;

    private PlayerProfile profile;

    public Player(String uuid) {
        this.uuid = uuid;
    }

    public String getUuid() {
        return uuid;
    }

    public PlayerProfile getProfile() {
        return profile;
    }

    public void setProfile(PlayerProfile profile) {
        this.profile = profile;
    }
}
