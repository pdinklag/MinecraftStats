package de.pdinklag.mcstats.util;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.stream.Collectors;

public class StreamUtils {
    public static String readStreamFully(InputStream in) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(in));
        String streamContents = br.lines().collect(Collectors.joining("\n"));
        br.close();
        return streamContents;
    }
}
