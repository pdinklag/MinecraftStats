package de.pdinklag.mcstats.bukkit;

import java.io.InputStream;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

import org.bukkit.scheduler.BukkitRunnable;

import de.pdinklag.mcstats.util.ResourceUtils;

public class UnpackWebFilesTask extends BukkitRunnable {
    private static final String WEB_RESOURCE_DIR = "www";
    private static final int WEB_FILENAME_PREFIX = WEB_RESOURCE_DIR.length() + 2; // enclodes by slashes ("/www/")

    private final MinecraftStatsPlugin plugin;
    private final Path documentRoot;

    public UnpackWebFilesTask(MinecraftStatsPlugin plugin, Path documentRoot) {
        this.plugin = plugin;
        this.documentRoot = documentRoot;
    }

    @Override
    public void run() {
        // unpack web files
        try {
            for(String resource : ResourceUtils.getResourceFilenames(getClass().getClassLoader(), WEB_RESOURCE_DIR)) {
                final Path destPath = documentRoot.resolve(resource.substring(WEB_FILENAME_PREFIX));
                if(destPath.getFileName().toString().contains(".")) {
                    // this is a file, extract it
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
            plugin.onWebPathInitialized();
        } catch(Exception e) {
            plugin.getLogger().severe(e.getMessage());
        }
    }
}
