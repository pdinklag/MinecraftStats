package de.pdinklag.mcstats.cli;

import java.nio.file.Files;
import java.nio.file.Path;

import org.json.JSONObject;

import de.pdinklag.mcstats.Updater;

/**
 * The entry point for the MinecraftStats command-line interface.
 */
public class MinecraftStatsCLI {
    /**
     * The main method.
     * @param args the command-line arguments passed to the application
     */
    public static void main(String[] args) {
        if(args.length > 0) {
            try {
                // load config
                JSONObject configJson = new JSONObject(Files.readString(Path.of(args[0])));
                JSONConfig config = new JSONConfig(configJson);

                // run updater
                Updater updater = new Updater(config, new StdoutLogWriter());
                updater.run();
            } catch(Exception e)
            {
                e.printStackTrace();
            }
        } else {
            System.err.println("you need to pass a config filename!");
        }
    }
}
