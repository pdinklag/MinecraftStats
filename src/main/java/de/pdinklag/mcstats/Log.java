package de.pdinklag.mcstats;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Path;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * The MinecraftStats log.
 */
public class Log {
    private static final DateTimeFormatter DATE_FORMAT = DateTimeFormatter.ofPattern("dd-MM-yyyy HH:mm:ss");
    private static Log current;

    public static Log getCurrent() {
        return current;
    }

    public static void setCurrent(Log current) {
        Log.current = current;
    }

    /**
     * The available log categories.
     */
    public enum Category {
        // generic message types that should be visible in the console
        PROGRESS(true), // generic progress updates
        CONFIG(true), // messages related to the configuration
        ERROR(true), // error messages, typically accompanied by a stacktrace

        // message types specific to certain parts of MinecraftStats
        EVENTS,
        ;

        private final boolean console;

        private Category(boolean console) {
            this.console = console;
        }

        private Category() {
            this(false);
        }

        public boolean isConsole() {
            return console;
        }
    }

    private static String formatMessage(Category category, String message) {
        return "(#" + category.toString() + ") " + message;
    }

    private final BufferedWriter fileWriter;
    private final ConsoleWriter console;
    private final boolean[] logToConsole;

    public Log(Path filePath, ConsoleWriter console) throws IOException {
        this.console = console;

        this.logToConsole = new boolean[Category.values().length];
        this.logToConsole[Category.PROGRESS.ordinal()] = true;
        this.logToConsole[Category.CONFIG.ordinal()] = true;
        this.logToConsole[Category.ERROR.ordinal()] = true;

        this.fileWriter = new BufferedWriter(new FileWriter(filePath.toFile()));
    }

    private void writeFileLine(Category category, String message) {
        try {
            fileWriter.write("[");
            fileWriter.write(LocalDateTime.now().format(DATE_FORMAT));
            fileWriter.write("] ");
            fileWriter.write(formatMessage(category, message));
            fileWriter.newLine();
        } catch (IOException e) {
            console.writeError("error trying to log to file", e);
        }
    }

    private void flushFile() {
        try {
            fileWriter.flush();
        } catch (IOException e) {
            console.writeError("error trying to flush log file", e);
        }
    }

    public void writeLine(Category category, String message) {
        writeFileLine(category, message);
        flushFile();

        if (logToConsole[category.ordinal()]) {
            console.writeLine(message);
        }
    }

    public void writeError(String message, Throwable e) {
        writeFileLine(Category.ERROR, message);
        e.printStackTrace(new PrintWriter(fileWriter));
        flushFile();

        if (logToConsole[Category.ERROR.ordinal()]) {
            console.writeError(message, e);
        }
    }

    public void close() throws IOException {
        fileWriter.close();
    }
}
