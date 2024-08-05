package de.pdinklag.mcstats.cli;

import de.pdinklag.mcstats.ConsoleWriter;

public class StdoutConsoleWriter implements ConsoleWriter {
    @Override
    public void writeLine(String line) {
        System.out.println(line);
    }

    @Override
    public void writeError(String line, Throwable e) {
        System.err.println(line);
        if (e != null) {
            e.printStackTrace(System.err);
        }
    }
}
