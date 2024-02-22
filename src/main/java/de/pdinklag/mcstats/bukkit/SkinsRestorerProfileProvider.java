package de.pdinklag.mcstats.bukkit;

import java.util.Optional;
import java.util.UUID;

import de.pdinklag.mcstats.AccountType;
import de.pdinklag.mcstats.Player;
import de.pdinklag.mcstats.PlayerProfile;
import de.pdinklag.mcstats.PlayerProfileProvider;
import net.skinsrestorer.api.PropertyUtils;
import net.skinsrestorer.api.SkinsRestorer;
import net.skinsrestorer.api.SkinsRestorerProvider;
import net.skinsrestorer.api.property.SkinProperty;

public class SkinsRestorerProfileProvider implements PlayerProfileProvider {
    private final SkinsRestorer api;

    public SkinsRestorerProfileProvider() {
        api = SkinsRestorerProvider.get();
    }

    @Override
    public PlayerProfile getPlayerProfile(Player player) {
        final Optional<SkinProperty> skinProperty = api.getPlayerStorage()
                .getSkinOfPlayer(UUID.fromString(player.getUuid()));
        if (skinProperty.isPresent()) {
            player.setAccountType(AccountType.MOJANG);
            return new PlayerProfile(
                    PropertyUtils.getSkinProfileData(skinProperty.get()).getProfileName(),
                    PropertyUtils.getSkinTextureUrlStripped(skinProperty.get()),
                    System.currentTimeMillis());
        } else if (player.getAccountType().maybeMojangAccount()) {
            player.setAccountType(AccountType.OFFLINE);
        }
        return player.getProfile();
    }
}
