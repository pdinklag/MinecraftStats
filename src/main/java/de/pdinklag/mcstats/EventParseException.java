package de.pdinklag.mcstats;

public class EventParseException extends RuntimeException {
    public EventParseException() {
    }

    public EventParseException(String message) {
        super(message);
    }

    public EventParseException(Throwable cause) {
        super(cause);
    }

    public EventParseException(String message, Throwable cause) {
        super(message, cause);
    }
    
}
