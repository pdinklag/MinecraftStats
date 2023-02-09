package de.pdinklag.mcstats;

/**
 * Interface for log writers.
 */
public interface LogWriter {
    /**
     * Writes a line to the log.
     * @param line the line to write
     */
    public void writeLine(String line);

    /**
     * Writes an error line and a stack trace to the log.
     * @param line the message to write
     * @param e the throwable
     */
    public void writeError(String line, Throwable e);
}
