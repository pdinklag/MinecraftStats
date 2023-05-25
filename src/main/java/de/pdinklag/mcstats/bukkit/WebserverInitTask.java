package de.pdinklag.mcstats.bukkit;

import java.io.InputStream;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

import org.bukkit.scheduler.BukkitRunnable;

import de.pdinklag.mcstats.util.ResourceUtils;

public class WebserverInitTask extends BukkitRunnable {
    private static final String WEB_RESOURCE_DIR = "www";
    private static final int WEB_FILENAME_PREFIX = WEB_RESOURCE_DIR.length() + 2; // enclodes by slashes ("/www/")

    private final MinecraftStatsPlugin plugin;
    private final Webserver webserver;

    public WebserverInitTask(MinecraftStatsPlugin plugin, Webserver webserver) {
        this.plugin = plugin;
        this.webserver = webserver;
    }

    @Override
    public void run() {
        final Path target = webserver.getTarget();

        // unpack web files
        try {
            for(String resource : ResourceUtils.getResourceFilenames(getClass().getClassLoader(), WEB_RESOURCE_DIR)) {
                final Path destPath = target.resolve(resource.substring(WEB_FILENAME_PREFIX));
                if(destPath.getFileName().toString().contains(".")) {
                    // this is a file, extract it
                    // TODO: only do this if the destination file does not exist OR the MinecraftStats version is newer than the current (which is not yet stored anywhere)
                    try(
                        InputStream in = getClass().getResourceAsStream(resource);
                        OutputStream out = Files.newOutputStream(destPath, StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING, StandardOpenOption.WRITE)
                    ) {
                        out.write(in.readAllBytes());
                    }
                } else {
                    // this is a directory, create it
                    Files.createDirectories(destPath);
                }
            }
            plugin.onTargetInitialized();
        } catch(Exception e) {
            plugin.getLogger().severe(e.getMessage());
        }
    }
}
