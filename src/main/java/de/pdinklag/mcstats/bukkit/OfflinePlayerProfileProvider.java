package de.pdinklag.mcstats.bukkit;

import java.util.UUID;

import org.bukkit.OfflinePlayer;
import org.bukkit.Server;

import de.pdinklag.mcstats.Player;
import de.pdinklag.mcstats.PlayerProfile;
import de.pdinklag.mcstats.PlayerProfileProvider;

public class OfflinePlayerProfileProvider implements PlayerProfileProvider {
    private final Server server;

    public OfflinePlayerProfileProvider(Server server) {
        this.server = server;
    }

    @Override
    public PlayerProfile getPlayerProfile(Player player) {
        OfflinePlayer offlinePlayer = server.getOfflinePlayer(UUID.fromString(player.getUuid()));
        if(offlinePlayer != null) {
            return new PlayerProfile(offlinePlayer.getName(), null);
        } else {
            return player.getProfile();
        }
    }
}
