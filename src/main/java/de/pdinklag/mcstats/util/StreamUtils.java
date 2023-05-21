package de.pdinklag.mcstats.util;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.stream.Collectors;

/**
 * Utilities related to streams.
 */
public class StreamUtils {
    /**
     * Fully reads the input stream into a string.
     * @param in the input stream
     * @return the contents of the stream
     * @throws IOException in case an IO error occurs
     */
    public static String readStreamFully(InputStream in) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(in));
        String streamContents = br.lines().collect(Collectors.joining("\n"));
        br.close();
        return streamContents;
    }
}
