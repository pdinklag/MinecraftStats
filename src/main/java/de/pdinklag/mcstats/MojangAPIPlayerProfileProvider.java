package de.pdinklag.mcstats;

import de.pdinklag.mcstats.mojang.API;
import de.pdinklag.mcstats.mojang.APIRequestException;

/**
 * Provides player profiles via the Mojang API.
 */
public class MojangAPIPlayerProfileProvider implements PlayerProfileProvider {
    /**
     * Constructs a new provider.
     */
    public MojangAPIPlayerProfileProvider() {
    }

    @Override
    public PlayerProfile getPlayerProfile(Player player) {
        try {
            return API.requestPlayerProfile(player.getUuid());
        } catch(APIRequestException e) {
            e.printStackTrace();
            return player.getProfile();
        }
    }
}
