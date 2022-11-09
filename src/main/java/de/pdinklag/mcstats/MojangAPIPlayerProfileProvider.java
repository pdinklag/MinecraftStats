package de.pdinklag.mcstats;

import de.pdinklag.mcstats.mojang.API;

public class MojangAPIPlayerProfileProvider implements PlayerProfileProvider {
    public MojangAPIPlayerProfileProvider() {
    }

    @Override
    public PlayerProfile getPlayerProfile(Player player) {
        try {
            return API.requestPlayerProfile(player.getUuid());
        } catch(Exception e) {
            e.printStackTrace();
            return player.getProfile();
        }
    }
}
