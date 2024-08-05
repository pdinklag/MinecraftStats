package de.pdinklag.mcstats.bukkit;

import de.pdinklag.mcstats.Log;
import de.pdinklag.mcstats.PlayerProfileProviderList;
import de.pdinklag.mcstats.Updater;

public class BukkitUpdater extends Updater {
    private final MinecraftStatsPlugin plugin;

    public BukkitUpdater(MinecraftStatsPlugin plugin, BukkitConfig config) {
        super(config);
        this.plugin = plugin;
    }

    @Override
    protected void gatherLocalProfileProviders(PlayerProfileProviderList providers) {
        super.gatherLocalProfileProviders(providers);
        providers.addFirst(new OfflinePlayerProfileProvider(plugin.getServer()));
    }

    @Override
    protected String getServerMotd() {
        return plugin.getServer().getMotd();
    }

    @Override
    protected String getVersion() {
        return plugin.getDescription().getVersion();
    }

    @Override
    public void run() {
        super.run();
        Log.getCurrent().writeLine(Log.Category.PROGRESS, "Web frontend updated.");
    }
}
