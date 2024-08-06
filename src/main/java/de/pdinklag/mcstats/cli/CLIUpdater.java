package de.pdinklag.mcstats.cli;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.CharacterCodingException;
import java.nio.charset.CharsetDecoder;
import java.nio.charset.CodingErrorAction;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Properties;

import de.pdinklag.mcstats.Config;
import de.pdinklag.mcstats.ConsoleWriter;
import de.pdinklag.mcstats.DataSource;
import de.pdinklag.mcstats.Log;
import de.pdinklag.mcstats.Updater;

public class CLIUpdater extends Updater {
    public CLIUpdater(Config config) {
        super(config);
    }

    @Override
    protected String getServerMotd() {
        for (DataSource dataSource : config.getDataSources()) {
            final Path propertiesPath = dataSource.getServerPath().resolve("server.properties");
            if (Files.exists(propertiesPath)) {
                final Properties properties = new Properties();
                final CharsetDecoder decoder = StandardCharsets.UTF_8.newDecoder()
                        .onMalformedInput(CodingErrorAction.REPORT).onUnmappableCharacter(CodingErrorAction.REPORT);
                try (final InputStream fis = Files.newInputStream(propertiesPath)) {
                    properties.load(new InputStreamReader(fis, decoder));
                } catch (CharacterCodingException e) {
                    Log.getCurrent().writeLine(Log.Category.PROGRESS,
                            "seems like the server.properties file is not encoded in UTF-8, trying ISO-8859-1");
                    try (final BufferedReader reader = Files.newBufferedReader(propertiesPath,
                            StandardCharsets.ISO_8859_1)) {
                        properties.load(reader);
                    } catch (IOException e1) {
                    }
                } catch (IOException e) {
                }
                final String motd = properties.getProperty("motd");
                if (motd != null) {
                    return motd;
                }
            }
        }
        return null;
    }

    @Override
    protected String getVersion() {
        return MinecraftStatsCLI.getVersion();
    }

    @Override
    public boolean run(ConsoleWriter consoleWriter) {
        if (super.run(consoleWriter)) {
            Log.getCurrent().writeLine(Log.Category.PROGRESS, "update finished");
            return true;
        } else {
            return false;
        }
    }
}
