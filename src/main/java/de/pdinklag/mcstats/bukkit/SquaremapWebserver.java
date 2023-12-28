package de.pdinklag.mcstats.bukkit;

import java.nio.file.Path;

import org.bukkit.configuration.Configuration;
import org.bukkit.plugin.Plugin;

public class SquaremapWebserver extends PluginWebserver {
    public static final String PLUGIN_NAME = "squaremap";

    private static final String DEFAULT_WEBPATH = "web";

    private final Path documentRoot;

    public SquaremapWebserver(Plugin squaremapPlugin) {
        final Path squaremapPath = squaremapPlugin.getDataFolder().toPath().toAbsolutePath();

        String webPath;
        try {
            final Configuration squaremapConfig = squaremapPlugin.getConfig();
            webPath = squaremapConfig.getString("settings.web-directory.path", DEFAULT_WEBPATH);
        } catch(Exception e) {
            e.printStackTrace();
            webPath = DEFAULT_WEBPATH;
        }

        this.documentRoot = squaremapPath.resolve(webPath);
    }

    @Override
    public Path getDocumentRoot() {
        return documentRoot;
    }
}
