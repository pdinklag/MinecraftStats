package de.pdinklag.mcstats.bukkit;

import org.bukkit.Server;

import de.pdinklag.mcstats.Player;
import de.pdinklag.mcstats.PlayerProfile;
import de.pdinklag.mcstats.PlayerProfileProvider;

public class BukkitPlayerProfileProvider implements PlayerProfileProvider {
    private final Server server;

    public BukkitPlayerProfileProvider(Server server) {
        this.server = server;
    }

    @Override
    public PlayerProfile getPlayerProfile(Player player) {
        return player.getProfile(); // TODO: use Bukkit API (PlayerProfile if available, OfflinePlayer as fallback)!
    }
}
