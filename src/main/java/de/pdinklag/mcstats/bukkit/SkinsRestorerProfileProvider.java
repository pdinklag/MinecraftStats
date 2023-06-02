package de.pdinklag.mcstats.bukkit;

import de.pdinklag.mcstats.AccountType;
import de.pdinklag.mcstats.LogWriter;
import de.pdinklag.mcstats.Player;
import de.pdinklag.mcstats.PlayerProfile;
import de.pdinklag.mcstats.PlayerProfileProvider;
import net.skinsrestorer.api.SkinsRestorerAPI;
import net.skinsrestorer.api.model.MojangProfileResponse;
import net.skinsrestorer.api.property.IProperty;

public class SkinsRestorerProfileProvider implements PlayerProfileProvider {
    private final SkinsRestorerAPI api;
    private final LogWriter log;

    public SkinsRestorerProfileProvider(LogWriter log) {
        this.log = log;

        api = SkinsRestorerAPI.getApi();
    }

    @Override
    public PlayerProfile getPlayerProfile(Player player) {
        final PlayerProfile currentProfile = player.getProfile();
        if (currentProfile.hasName()) {
            final String skinName = api.getSkinName(currentProfile.getName());
            if (skinName != null) {
                final IProperty skinData = api.getSkinData(skinName);
                if (skinData != null) {
                    final String skin = api.getSkinTextureUrlStripped(skinData);
                    return new PlayerProfile(currentProfile.getName(), skin, System.currentTimeMillis());
                }
            }
        }

        if (player.getAccountType().maybeMojangAccount()) {
            final IProperty skinsRestorerProfile = api.getProfile(player.getUuid());
            if (skinsRestorerProfile != null) {
                player.setAccountType(AccountType.MOJANG);
                final MojangProfileResponse mojangProfile = api.getSkinProfileData(skinsRestorerProfile);
                return new PlayerProfile(mojangProfile.getProfileName(),
                        mojangProfile.getTextures().getSKIN().getStrippedUrl(), System.currentTimeMillis());
            } else {
                player.setAccountType(AccountType.OFFLINE);
            }
        }
        return currentProfile;
    }
}
