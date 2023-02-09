package de.pdinklag.mcstats.util;

import java.nio.file.Path;

/**
 * Utilities regarding Minecraft servers.
 */
public class MinecraftServerUtils {
    /**
     * Gets the path to banned-players.json for the given server path.
     * 
     * @param serverPath the server path
     * @return the path to the server's banned-players.json
     */
    public static Path getBannedPlayersPath(Path serverPath) {
        return serverPath.resolve("banned-players.json");
    }

    /**
     * Gets the path to ops.json for the given server path.
     * 
     * @param serverPath the server path
     * @return the path to the server's ops.json
     */
    public static Path getOpsPath(Path serverPath) {
        return serverPath.resolve("ops.json");
    }

    /**
     * Gets the path to usercache.json for the given server path.
     * 
     * @param serverPath the server path
     * @return the path to the server's usercache.json
     */
    public static Path getUserCachePath(Path serverPath) {
        return serverPath.resolve("usercache.json");
    }
}
