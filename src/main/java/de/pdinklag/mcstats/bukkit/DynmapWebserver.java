package de.pdinklag.mcstats.bukkit;

import java.nio.file.Path;

import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.plugin.Plugin;

public class DynmapWebserver extends PluginWebserver {
    public static final String PLUGIN_NAME = "dynmap";
    
    private static final String CONFIG_FILENAME = "configuration.txt";
    private static final String DEFAULT_WEBPATH = "web";

    private final Path documentRoot;

    public DynmapWebserver(Plugin dynmapPlugin) {
        final Path dynmapPath = dynmapPlugin.getDataFolder().toPath().toAbsolutePath();
        
        String webPath;
        try {
            final YamlConfiguration dynmapConfig = YamlConfiguration.loadConfiguration(dynmapPath.resolve(CONFIG_FILENAME).toFile());
            webPath = dynmapConfig.getString("webpath", DEFAULT_WEBPATH);
        } catch(Exception e) {
            e.printStackTrace();
            webPath = DEFAULT_WEBPATH;
        }

        this.documentRoot = dynmapPath.resolve(webPath);
    }

    @Override
    public Path getDocumentRoot() {
        return documentRoot;
    }
}
