package de.pdinklag.mcstats.mojang;

public class APIException extends RuntimeException {
    public APIException() {
    }

    public APIException(String message) {
        super(message);
    }

    public APIException(Throwable cause) {
        super(cause);
    }

    public APIException(String message, Throwable cause) {
        super(message, cause);
    }
    
}
