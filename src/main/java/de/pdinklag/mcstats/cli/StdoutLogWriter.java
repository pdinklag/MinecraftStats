package de.pdinklag.mcstats.cli;

import de.pdinklag.mcstats.LogWriter;

public class StdoutLogWriter implements LogWriter {
    @Override
    public void writeLine(String line) {
        System.out.println(line);
    }

    @Override
    public void writeError(Throwable e) {
        e.printStackTrace();
    }
}
