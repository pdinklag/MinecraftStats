package de.pdinklag.mcstats.util;

import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.zip.GZIPOutputStream;

/**
 * Utilities related to file I/O.
 */
public class FileUtils {
    /**
     * Writes a gzipped string into the given file.
     * 
     * The file will be created if it does not yet exist, otherwise it will be overwritten.
     * 
     * @param path the path to the file to write
     * @param s the string to compress and write
     * @throws IOException in case an IO error occurs
     */
    public static void writeStringGzipped(Path path, String s) throws IOException {
        try (
                OutputStream fos = Files.newOutputStream(path, StandardOpenOption.WRITE,
                        StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING);
                GZIPOutputStream gzos = new GZIPOutputStream(fos);
                OutputStreamWriter writer = new OutputStreamWriter(gzos)) {

            writer.write(s);
            writer.flush();
        }
    }
}
