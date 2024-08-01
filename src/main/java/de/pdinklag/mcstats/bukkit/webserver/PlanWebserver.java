package de.pdinklag.mcstats.bukkit.webserver;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.bukkit.plugin.Plugin;


public class PlanWebserver extends PluginWebserver {
    private static final String CONFIG_FILENAME = "config.yml";
    private static final Pattern PUBLIC_HTML_PATTERN = Pattern.compile("Public_html_directory: \"(.+)\"");
    private static final String DEFAULT_HTML_PATH = "public_html";

    public PlanWebserver(Plugin plugin) {
        final Path pluginPath = plugin.getDataFolder().toPath().toAbsolutePath();
        final Path configPath = pluginPath.resolve(CONFIG_FILENAME);

        String htmlPath;
        try {
            final String config = Files.readString(configPath);
            final Matcher matcher = PUBLIC_HTML_PATTERN.matcher(config);
            if (matcher.find()) {
                htmlPath = matcher.group(1);
            } else {
                throw new RuntimeException(
                        "Failed to find Public_html_directory in Plan webserver config: " + configPath.toString());
            }
        } catch (Exception e) {
            e.printStackTrace();
            htmlPath = DEFAULT_HTML_PATH;
        }

        setDocumentRoot(pluginPath.resolve(htmlPath));
    }
}
