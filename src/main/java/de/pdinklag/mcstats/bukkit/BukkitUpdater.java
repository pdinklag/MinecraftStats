package de.pdinklag.mcstats.bukkit;

import java.util.Deque;

import de.pdinklag.mcstats.Log;
import de.pdinklag.mcstats.PlayerProfileProvider;
import de.pdinklag.mcstats.Updater;

public class BukkitUpdater extends Updater {
    private final MinecraftStatsPlugin plugin;
    private final BukkitConfig config;
    private boolean firstUpdate;

    public BukkitUpdater(MinecraftStatsPlugin plugin, BukkitConfig config) {
        super(config);
        this.plugin = plugin;
        this.config = config;
        this.firstUpdate = true;
    }

    @Override
    protected void gatherLocalProfileProviders(Deque<PlayerProfileProvider> providers) {
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

        if (firstUpdate) {
            Log.getCurrent().writeLine(
                    Log.Category.PROGRESS, "Web frontend updated. This will now happen every "
                            + config.getUpdateInterval() + " minute(s) without any further logging to the console.");
            firstUpdate = false;
        } else {
            Log.getCurrent().writeLine(
                    Log.Category.SILENT_PROGRESS, "Web frontend updated.");
        }
    }
}
