package de.pdinklag.mcstats.util;

public class ClientUtils {
    /**
     * Converts a timestamp for the client.
     * 
     * The client uses integer timestamps telling seconds since the epoch.
     * 
     * @param millis the timestamp in milliseconds since the epoch
     * @return the corresponding client timestamp
     */
    public static int convertTimestamp(long millis) {
        return (int)(millis / 1000L);
    }
}
