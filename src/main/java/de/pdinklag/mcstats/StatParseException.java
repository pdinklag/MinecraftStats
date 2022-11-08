package de.pdinklag.mcstats;

public class StatParseException extends RuntimeException {
    public StatParseException() {
    }

    public StatParseException(String message) {
        super(message);
    }

    public StatParseException(Throwable cause) {
        super(cause);
    }

    public StatParseException(String message, Throwable cause) {
        super(message, cause);
    }
    
}
