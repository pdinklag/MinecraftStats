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
        {
            // try BlueMap
            Plugin bluemapPlugin = pluginManager.getPlugin(BlueMapWebserver.PLUGIN_NAME);
            if (bluemapPlugin != null) {
                return new BlueMapWebserver(bluemapPlugin);
            }
        }
        {
            // try squaremap
            Plugin squaremapPlugin = pluginManager.getPlugin(SquaremapWebserver.PLUGIN_NAME);
            if (squaremapPlugin != null) {
                return new SquaremapWebserver(squaremapPlugin);
            }
        }
        return null;
    }

    public abstract Path getDocumentRoot();
}
