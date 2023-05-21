package de.pdinklag.mcstats.util;

import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.zip.GZIPOutputStream;

public class FileUtils {
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
