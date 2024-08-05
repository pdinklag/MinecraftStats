package de.pdinklag.mcstats.bukkit;

import org.bukkit.scheduler.BukkitRunnable;

import de.pdinklag.mcstats.util.ResourceUtils;

public class UnpackTask extends BukkitRunnable {
    private static final String STATS_RESOURCE_DIR = "stats";
    private static final String WEB_RESOURCE_DIR = "www";

    private final MinecraftStatsPlugin plugin;
    private final BukkitConfig config;

    public UnpackTask(MinecraftStatsPlugin plugin, BukkitConfig config) {
        this.plugin = plugin;
        this.config = config;
    }

    @Override
    public void run() {
        try {
            // unpack
            ResourceUtils.extractResourcesToFiles(STATS_RESOURCE_DIR, config.getStatsPath());

            if(config.isUnpackWebFiles()) {
                ResourceUtils.extractResourcesToFiles(WEB_RESOURCE_DIR, config.getDocumentRoot());
            }

            // notify plugin
            plugin.onUnpackComplete();
        } catch(Exception e) {
            new LoggerConsoleWriter(plugin.getLogger()).writeError("Failed to unpack resources", e);
        }
    }
}
