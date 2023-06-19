package de.pdinklag.mcstats.bukkit;

import java.nio.file.Path;

import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.plugin.Plugin;

public class BlueMapWebserver extends PluginWebserver {
    public static final String PLUGIN_NAME = "BlueMap";
    
    private static final String CONFIG_FILENAME = "webserver.conf";
    private static final String DEFAULT_WEBROOT = "bluemap/web";

    private final Path documentRoot;

    public BlueMapWebserver(Plugin bluemapPlugin) {
        final Path bluemapPath = bluemapPlugin.getDataFolder().toPath().toAbsolutePath();
        
        String webRoot;
        try {
            final YamlConfiguration bluemapWebserverConfig = YamlConfiguration.loadConfiguration(bluemapPath.resolve(CONFIG_FILENAME).toFile());
            webRoot = bluemapWebserverConfig.getString("webroot", DEFAULT_WEBROOT);
        } catch(Exception e) {
            e.printStackTrace();
            webRoot = DEFAULT_WEBROOT;
        }

        this.documentRoot = bluemapPlugin.getServer().getWorldContainer().toPath().resolve(webRoot).toAbsolutePath();
    }

    @Override
    public Path getDocumentRoot() {
        return documentRoot;
    }
}
