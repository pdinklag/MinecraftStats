package de.pdinklag.mcstats.cli;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * The entry point for the MinecraftStats command-line interface.
 */
public class MinecraftStatsCLI {
    private static final DateTimeFormatter DATE_FORMAT = DateTimeFormatter.ofPattern("dd-MM-yyyy HH:mm:ss");

    private static String getJarFilename() {
        final File jarFile = new File(
                MinecraftStatsCLI.class.getProtectionDomain().getCodeSource().getLocation().getPath());
        return jarFile.getName();
    }

    /**
     * The main method.
     * 
     * @param args the command-line arguments passed to the application
     */
    public static void main(String[] args) {
        if (args.length > 0) {
            final StdoutLogWriter log = new StdoutLogWriter();
            try {
                // load config
                final Path configPath = Path.of(args[0]);
                if (Files.isRegularFile(configPath)) {
                    JSONConfig config = new JSONConfig(configPath);

                    // run updater
                    CLIUpdater updater = new CLIUpdater(config, log);
                    updater.run();

                    log.writeLine("[" + LocalDateTime.now().format(DATE_FORMAT) + "] update finished");
                } else {
                    System.err.println("Configuration file not found: " + configPath);
                    System.exit(1);
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        } else {
            System.err.println("Usage: java -jar " + getJarFilename() + " <config>");
            System.exit(1);
        }
    }
}
