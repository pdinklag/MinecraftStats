package de.pdinklag.mcstats.bukkit;

import java.nio.file.Path;

import org.bukkit.Server;
import org.bukkit.plugin.Plugin;
import org.bukkit.plugin.PluginManager;

public class PluginWebserver {
    private static final String DYNMAP_PLUGIN_NAME = "dynmap";
    private static final String DYNMAP_WEB_FOLDER_NAME = "web";

    public static PluginWebserver find(Server server) {
        final PluginManager pluginManager = server.getPluginManager();
        {
            // try dynmap
            Plugin dynmapPlugin = pluginManager.getPlugin(DYNMAP_PLUGIN_NAME);
            if (dynmapPlugin != null) {
                final Path root = Path.of(dynmapPlugin.getDataFolder().getAbsolutePath()).resolve(DYNMAP_WEB_FOLDER_NAME);
                return new PluginWebserver(root);
            }
        }
        return null;
    }

    private final Path documentRoot;

    public PluginWebserver(Path documentRoot) {
        this.documentRoot = documentRoot;
    }

    public Path getDocumentRoot() {
        return documentRoot;
    }
}
