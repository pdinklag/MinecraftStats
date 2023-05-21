package de.pdinklag.mcstats.bukkit;

import java.util.Set;

import org.bukkit.OfflinePlayer;

import de.pdinklag.mcstats.ExcludeUUIDPlayerFilter;

/**
 * A player filter that excludes players stated in by a set of offline players.
 */
public class BukkitPlayerFilter extends ExcludeUUIDPlayerFilter {
    /**
     * Constructs a filter.
     * 
     * @param excludedPlayers the set of Bukkit players to exclude
     */
    public BukkitPlayerFilter(Set<OfflinePlayer> excludedPlayers) {
        excludedPlayers.forEach(player -> {
            exclude(player.getUniqueId().toString());
        });
    }
}
