package de.pdinklag.mcstats;

/**
 * Interface for log writers.
 */
public interface LogWriter {
    /**
     * Writes a line to the log.
     * @param line the line to write.
     */
    public void writeLine(String line);

    /**
     * Writes an error to the log.
     * @param e the error
     */
    public void writeError(Throwable e);
}
