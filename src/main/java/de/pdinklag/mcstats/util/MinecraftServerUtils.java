package de.pdinklag.mcstats.util;

import java.nio.file.Path;

/**
 * Utilities regarding Minecraft servers.
 */
public class MinecraftServerUtils {
    /**
     * Gets the path to usercache.json for the given server path.
     * @param serverPath the server path
     * @return the path to the server's usercache.json
     */
    public static Path getUserCachePath(Path serverPath) {
        return serverPath.resolve("usercache.json");
    }
}
