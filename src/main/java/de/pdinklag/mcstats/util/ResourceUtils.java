package de.pdinklag.mcstats.util;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URISyntaxException;
import java.net.URL;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.List;
import java.util.jar.JarEntry;
import java.util.jar.JarFile;

public class ResourceUtils {
    public static List<String> getResourceFilenames(ClassLoader classLoader, String dirname)
            throws URISyntaxException, UnsupportedEncodingException, IOException {
        List<String> filenames = new ArrayList<>();

        if (!dirname.endsWith("/")) {
            dirname = dirname + "/";
        }

        final URL url = classLoader.getResource(dirname);
        if (url != null && url.getProtocol().equals("jar")) {
            final String path = url.getPath();
            final String jarPath = path.substring(5, path.indexOf("!"));
            try (JarFile jar = new JarFile(URLDecoder.decode(jarPath, StandardCharsets.UTF_8.name()))) {
                final Enumeration<JarEntry> entries = jar.entries();
                while (entries.hasMoreElements()) {
                    final String filename = entries.nextElement().getName();
                    if (filename.length() > dirname.length() && filename.startsWith(dirname)) {
                        filenames.add("/" + filename);
                    }
                }
            }
        }
        return filenames;
    }
}
