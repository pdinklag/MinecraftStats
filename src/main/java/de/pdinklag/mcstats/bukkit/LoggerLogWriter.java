package de.pdinklag.mcstats.bukkit;

import java.io.PrintWriter;
import java.io.StringWriter;
import java.util.logging.Logger;

import de.pdinklag.mcstats.LogWriter;

public class LoggerLogWriter implements LogWriter {
    private final Logger logger;

    public LoggerLogWriter(Logger logger) {
        this.logger = logger;
    }

    @Override
    public void writeLine(String line) {
        logger.info(line);
    }

    @Override
    public void writeError(String line, Throwable e) {
        StringWriter stackTrace = new StringWriter();
        PrintWriter stackTraceWriter = new PrintWriter(stackTrace);
        e.printStackTrace(stackTraceWriter);

        logger.warning(line + "\n" + stackTrace.toString());
    }
    
}
