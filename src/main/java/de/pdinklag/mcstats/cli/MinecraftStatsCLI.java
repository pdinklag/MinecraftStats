package de.pdinklag.mcstats.cli;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import de.pdinklag.mcstats.util.StreamUtils;

/**
 * The entry point for the MinecraftStats command-line interface.
 */
public class MinecraftStatsCLI {
    public static String getVersion() {
        try {
            return StreamUtils.readStreamFully(MinecraftStatsCLI.class.getResourceAsStream("/version.txt"));
        } catch (IOException e) {
            e.printStackTrace();
            return "0.0.0";
        }
    }

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
            final StdoutConsoleWriter consoleWriter = new StdoutConsoleWriter();
            try {
                // load config
                final Path configPath = Path.of(args[0]);
                if (Files.isRegularFile(configPath)) {
                    final JSONConfig config = new JSONConfig(configPath);

                    // run updater
                    final CLIUpdater updater = new CLIUpdater(config);
                    updater.run(consoleWriter);
                } else {
                    System.err.println("Configuration file not found: " + configPath);
                    System.exit(1);
                }
            } catch (Exception e) {
                consoleWriter.writeError("update failed", e);
            }
        } else {
            System.err.println("MinecraftStats " + getVersion());
            System.err.println("Usage: java -jar " + getJarFilename() + " <config>");
            System.exit(1);
        }
    }
}
