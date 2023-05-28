package de.pdinklag.mcstats.util;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.net.URISyntaxException;
import java.net.URL;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.List;
import java.util.jar.JarEntry;
import java.util.jar.JarFile;

/**
 * Utilities related to the JAR's resources.
 */
public class ResourceUtils {
    private static List<String> getResourceFilenames(String dirname)
            throws URISyntaxException, UnsupportedEncodingException, IOException {
        List<String> filenames = new ArrayList<>();

        if (!dirname.endsWith("/")) {
            dirname = dirname + "/";
        }

        final URL url = ResourceUtils.class.getClassLoader().getResource(dirname);
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

    public static void extractResourcesToFiles(String dirname, Path dest)
            throws URISyntaxException, UnsupportedEncodingException, IOException {
        final int filenamePrefixLength = dirname.length() + 2;

        for (String resource : getResourceFilenames(dirname)) {
            final Path destPath = dest.resolve(resource.substring(filenamePrefixLength));
            if (destPath.getFileName().toString().contains(".")) {
                Files.createDirectories(destPath.getParent());
                try (
                        InputStream in = ResourceUtils.class.getResourceAsStream(resource);
                        OutputStream out = Files.newOutputStream(destPath, StandardOpenOption.CREATE,
                                StandardOpenOption.TRUNCATE_EXISTING, StandardOpenOption.WRITE)) {
                    out.write(in.readAllBytes());
                }
            }
        }
    }
}
