package de.pdinklag.mcstats;

import de.pdinklag.mcstats.mojang.API;
import de.pdinklag.mcstats.mojang.APIRequestException;
import de.pdinklag.mcstats.mojang.EmptyResponseException;

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
        if (player.getAccountType().maybeMojangAccount()) {
            try {
                PlayerProfile profile = API.requestPlayerProfile(player.getUuid());
                player.setAccountType(AccountType.MOJANG);
                return profile;
            } catch (EmptyResponseException e) {
                player.setAccountType(AccountType.OFFLINE);
            } catch (APIRequestException e) {
                log.writeError("Mojang API profile request for player failed: " + player.getUuid(), e);
            }
        }
        return player.getProfile();
    }
}
