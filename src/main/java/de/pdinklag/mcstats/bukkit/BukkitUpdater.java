package de.pdinklag.mcstats.bukkit;

import org.bukkit.plugin.Plugin;

import de.pdinklag.mcstats.Config;
import de.pdinklag.mcstats.LogWriter;
import de.pdinklag.mcstats.PlayerProfileProvider;
import de.pdinklag.mcstats.PlayerProfileProviderList;
import de.pdinklag.mcstats.Updater;
import de.pdinklag.mcstats.util.Version;

public class BukkitUpdater extends Updater {
    private static final String SKINS_RESTORER_PLUGIN_NAME = "SkinsRestorer";
    private static final Version SKINS_RESTORER_MIN_VERSION = new Version(14, 2, 2);

    private final MinecraftStatsPlugin plugin;
    private boolean isSkinsRestorerAvailable;

    public BukkitUpdater(MinecraftStatsPlugin plugin, Config config, LogWriter log) {
        super(config, log);
        this.plugin = plugin;

        isSkinsRestorerAvailable = false;
        final Plugin skinsRestorerPlugin = plugin.getServer().getPluginManager()
                .getPlugin(SKINS_RESTORER_PLUGIN_NAME);
        if (skinsRestorerPlugin != null) {
            try {
                final Version skinsRestorerVersion = Version.parse(skinsRestorerPlugin.getDescription().getVersion());
                if (skinsRestorerVersion.compareTo(SKINS_RESTORER_MIN_VERSION) > 0) {
                    isSkinsRestorerAvailable = true;
                    log.writeLine("Using SkinsRestorer v" + skinsRestorerVersion);
                } else {
                    log.writeLine("SkinsRestorer v" + skinsRestorerVersion + " is not supported -- must be "
                            + SKINS_RESTORER_MIN_VERSION + " or later!");
                }
            } catch (Exception e) {
                log.writeError(
                        "Failed to parse SkinsRestorer version: " + skinsRestorerPlugin.getDescription().getVersion(),
                        e);
            }
        }
    }

    @Override
    protected PlayerProfileProvider getAuthenticProfileProvider() {
        if (isSkinsRestorerAvailable) {
            return new SkinsRestorerProfileProvider(log);
        } else {
            return super.getAuthenticProfileProvider();
        }
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
        log.writeLine("Web frontend updated.");
    }
}
