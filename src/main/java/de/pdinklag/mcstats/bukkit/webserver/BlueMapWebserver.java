package de.pdinklag.mcstats.bukkit.webserver;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.bukkit.plugin.Plugin;

public class BlueMapWebserver extends PluginWebserver {
    private static final String CONFIG_FILENAME = "webserver.conf";
    private static final Pattern WEBROOT_PATTERN = Pattern.compile("webroot: \"(.+)\"");
    private static final String DEFAULT_WEBROOT = "bluemap/web";

    public BlueMapWebserver(Plugin plugin) {
        final Path bluemapPath = plugin.getDataFolder().toPath().toAbsolutePath();
        final Path bluemapWebserverConfigPath = bluemapPath.resolve(CONFIG_FILENAME);

        String webRoot;
        try {
            final String bluemapWebserverConfig = Files.readString(bluemapWebserverConfigPath);
            final Matcher matcher = WEBROOT_PATTERN.matcher(bluemapWebserverConfig);
            if (matcher.find()) {
                webRoot = matcher.group(1);
            } else {
                throw new RuntimeException(
                        "Failed to find webroot in BlueMap webserver config: " + bluemapWebserverConfigPath.toString());
            }
        } catch (Exception e) {
            e.printStackTrace();
            webRoot = DEFAULT_WEBROOT;
        }

        setDocumentRoot(plugin.getServer().getWorldContainer().toPath().resolve(webRoot).toAbsolutePath());
    }
}
