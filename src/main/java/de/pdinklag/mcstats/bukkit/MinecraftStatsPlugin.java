package de.pdinklag.mcstats.bukkit;

import org.bukkit.plugin.java.JavaPlugin;

import de.pdinklag.mcstats.util.MinecraftServerUtils;

/**
 * The entry point of the MinecraftStats Bukkit plugin.
 */
public class MinecraftStatsPlugin extends JavaPlugin {
    private static final String DATABASE_DIRNAME = "data";
    private static final long TICKS_PER_MINUTE = 60L * MinecraftServerUtils.TICKS_PER_SECOND;

    private BukkitConfig config;
    private BukkitUpdater updater;
    private BukkitUpdateTask updateTask;

    @Override
    public void onEnable() {
        // load config
        saveDefaultConfig();
        config = new BukkitConfig(getServer(), getConfig());

        // detect webserver if necessary
        if(config.getDatabasePath() == null) {
            final Webserver webserver = WebserverDetection.findWebserver(getServer());
            if(webserver != null) {
                config.setDatabasePath(webserver.getTarget().resolve(DATABASE_DIRNAME));
                new WebserverInitTask(this, webserver).runTaskAsynchronously(this);
            } else {
                getLogger().warning("No database directory specified -- please state one explictly, or install a plugin featuring a webserver!");
            }
        } else {
            onTargetInitialized();
        }
    }

    void onTargetInitialized() {
        getLogger().info(config.getDatabasePath().toAbsolutePath().toString());

        updater = new BukkitUpdater(getServer(), config, new LoggerLogWriter(getLogger()));
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
