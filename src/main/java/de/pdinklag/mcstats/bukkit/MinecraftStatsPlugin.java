package de.pdinklag.mcstats.bukkit;

import java.nio.file.Path;

import org.bukkit.plugin.java.JavaPlugin;

import de.pdinklag.mcstats.util.MinecraftServerUtils;

/**
 * The entry point of the MinecraftStats Bukkit plugin.
 */
public class MinecraftStatsPlugin extends JavaPlugin {
    private static final long TICKS_PER_MINUTE = 60L * MinecraftServerUtils.TICKS_PER_SECOND;

    BukkitConfig config;
    private BukkitUpdater updater;
    private BukkitUpdateTask updateTask;

    @Override
    public void onEnable() {
        // load config
        saveDefaultConfig();
        config = new BukkitConfig(this);

        // detect webserver if necessary
        if(config.getDocumentRoot() == null) {
            final PluginWebserver webserver = PluginWebserver.find(getServer());
            if(webserver != null) {
                final Path documentRoot = webserver.getDocumentRoot().resolve(config.getWebSubdir());
                config.setDocumentRoot(documentRoot);
            } else {
                getLogger().warning("No document root specified -- please state one explictly in the configuration, or install a supported plugin featuring a webserver!");
                return;
            }
        }

        // unpack what's necessary and then continue
        new UnpackTask(this, config).runTaskAsynchronously(this);
    }

    void onUnpackComplete() {
        updater = new BukkitUpdater(this, config, new LoggerLogWriter(getLogger()));
        updateTask = new BukkitUpdateTask(updater);
        updateTask.runTaskTimerAsynchronously(this, 0, TICKS_PER_MINUTE * config.getUpdateInterval());
    }

    @Override
    public void onDisable() {
        if(updateTask != null) {
            updateTask.cancel();
        }
    }
}
