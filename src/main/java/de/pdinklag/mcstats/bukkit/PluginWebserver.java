package de.pdinklag.mcstats.bukkit;

import java.nio.file.Path;

import org.bukkit.Server;
import org.bukkit.plugin.Plugin;
import org.bukkit.plugin.PluginManager;

public abstract class PluginWebserver {
    public static PluginWebserver find(Server server) {
        final PluginManager pluginManager = server.getPluginManager();
        {
            // try dynmap
            Plugin dynmapPlugin = pluginManager.getPlugin(DynmapWebserver.PLUGIN_NAME);
            if (dynmapPlugin != null) {
                return new DynmapWebserver(dynmapPlugin);
            }
        }
        return null;
    }

    public abstract Path getDocumentRoot();
}
