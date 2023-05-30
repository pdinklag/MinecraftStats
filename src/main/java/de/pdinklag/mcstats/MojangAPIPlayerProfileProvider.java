package de.pdinklag.mcstats;

import de.pdinklag.mcstats.mojang.API;
import de.pdinklag.mcstats.mojang.APIRequestException;

/**
 * Provides player profiles via the Mojang API.
 */
public class MojangAPIPlayerProfileProvider implements PlayerProfileProvider {
    private final LogWriter log;

    /**
     * Constructs a new provider.
     */
    public MojangAPIPlayerProfileProvider(LogWriter log) {
        this.log = log;
    }

    @Override
    public PlayerProfile getPlayerProfile(Player player) {
        try {
            PlayerProfile profile = API.requestPlayerProfile(player.getUuid());
            if(profile != null) {
                return profile;
            } else {
                log.writeLine("empty Mojang API response for player: " + player.getUuid());
            }
        } catch(APIRequestException e) {
            log.writeError("Mojang API profile request for player failed: " + player.getUuid(), e);
        }
        return player.getProfile();
    }
}
