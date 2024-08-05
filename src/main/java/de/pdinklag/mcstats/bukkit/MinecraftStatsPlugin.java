package de.pdinklag.mcstats.bukkit;

import java.io.IOException;
import java.nio.file.Path;

import org.bukkit.plugin.java.JavaPlugin;

import de.pdinklag.mcstats.ConsoleWriter;
import de.pdinklag.mcstats.Log;
import de.pdinklag.mcstats.bukkit.webserver.PluginWebserver;
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

        // initialize logging
        ConsoleWriter consoleWriter = new LoggerConsoleWriter(getLogger());
        try {
            Log.setCurrent(new Log(config.getLogfilePath(), consoleWriter));
        } catch (IOException ex) {
            consoleWriter.writeError("failed to initialize logging", ex);
            return;
        }

        // detect webserver if necessary
        if (config.getDocumentRoot() == null) {
            final PluginWebserver webserver = PluginWebserver.find(getServer());
            if (webserver != null) {
                Log.getCurrent().writeLine(Log.Category.CONFIG,
                        "Exporting to auto-detected webserver document root: "
                                + webserver.getDocumentRoot().toAbsolutePath());

                final Path documentRoot = webserver.getDocumentRoot().resolve(config.getWebSubdir());
                config.setDocumentRoot(documentRoot);
            } else {
                Log.getCurrent().writeLine(Log.Category.CONFIG,
                        "No document root specified -- please state one explictly in the configuration, or install a supported plugin featuring a webserver!");
                return;
            }
        }

        // unpack what's necessary and then continue
        new UnpackTask(this, config).runTaskAsynchronously(this);
    }

    void onUnpackComplete() {
        updater = new BukkitUpdater(this, config);
        updateTask = new BukkitUpdateTask(updater);
        updateTask.runTaskTimerAsynchronously(this, 0, TICKS_PER_MINUTE * config.getUpdateInterval());
    }

    @Override
    public void onDisable() {
        if (updateTask != null) {
            updateTask.cancel();
        }
    }
}
