package de.pdinklag.mcstats.util;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Properties;

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

    /**
     * Gets the path to server-icon.png for the given server path.
     * 
     * @param serverPath the server path
     * @return the path to the server's icon
     */
    public static Path getServerIconPath(Path serverPath) {
        return serverPath.resolve("server-icon.png");
    }

    /**
     * Gets the MOTD from a Minecraft server's server.properties file.
     * 
     * @param serverPath the server path
     * @return the value of the MOTD field, if any
     */
    public static String getMOTD(Path serverPath) {
        final Path propertiesPath = serverPath.resolve("server.properties");
        if (Files.exists(propertiesPath)) {
            final Properties properties = new Properties();
            try (final InputStream fis = Files.newInputStream(propertiesPath)) {
                properties.load(fis);
            } catch (IOException e) {
                return null;
            }
            return properties.getProperty("motd");
        } else {
            return null;
        }
    }
}
