package de.pdinklag.mcstats.bukkit.webserver;

import java.nio.file.Path;

import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.plugin.Plugin;

public class DynmapWebserver extends PluginWebserver {
    private static final String CONFIG_FILENAME = "configuration.txt";
    private static final String DEFAULT_WEBPATH = "web";

    public DynmapWebserver(Plugin plugin) {
        final Path pluginPath = plugin.getDataFolder().toPath().toAbsolutePath();

        String webPath;
        try {
            final YamlConfiguration config = YamlConfiguration
                    .loadConfiguration(pluginPath.resolve(CONFIG_FILENAME).toFile());
            webPath = config.getString("webpath", DEFAULT_WEBPATH);
        } catch (Exception e) {
            e.printStackTrace();
            webPath = DEFAULT_WEBPATH;
        }

        setDocumentRoot(pluginPath.resolve(webPath));
    }
}
