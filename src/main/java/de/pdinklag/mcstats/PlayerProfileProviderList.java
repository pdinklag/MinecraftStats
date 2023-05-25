package de.pdinklag.mcstats;

import java.util.LinkedList;

/**
 * Provides a player profile by trying a list of providers.
 */
public class PlayerProfileProviderList implements PlayerProfileProvider {
    private final LinkedList<PlayerProfileProvider> providers = new LinkedList<>();

    @Override
    public PlayerProfile getPlayerProfile(Player player) {
        for(PlayerProfileProvider provider : providers) {
            PlayerProfile profile = provider.getPlayerProfile(player);
            if(profile.hasName()) {
                return profile;
            }
        }
        return player.getProfile();
    }

    public void addFirst(PlayerProfileProvider provider) {
        providers.addFirst(provider);
    }

    public void add(PlayerProfileProvider provider) {
        providers.add(provider);
    }
}
