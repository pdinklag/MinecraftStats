package de.pdinklag.mcstats.bukkit.webserver;

import java.nio.file.Path;

import org.bukkit.configuration.Configuration;
import org.bukkit.plugin.Plugin;

public class SquaremapWebserver extends PluginWebserver {
    private static final String DEFAULT_WEBPATH = "web";

    public SquaremapWebserver(Plugin plugin) {
        final Path pluginPath = plugin.getDataFolder().toPath().toAbsolutePath();

        String webPath;
        try {
            final Configuration config = plugin.getConfig();
            webPath = config.getString("settings.web-directory.path", DEFAULT_WEBPATH);
        } catch (Exception e) {
            e.printStackTrace();
            webPath = DEFAULT_WEBPATH;
        }

        setDocumentRoot(pluginPath.resolve(webPath));
    }
}
