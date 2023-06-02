package de.pdinklag.mcstats.mojang;

/**
 * An exception raised while processing a Mojang API request.
 */
public class APIRequestException extends RuntimeException {
    APIRequestException() {
    }

    APIRequestException(String message) {
        super(message);
    }

    APIRequestException(Throwable cause) {
        super(cause);
    }

    APIRequestException(String message, Throwable cause) {
        super(message, cause);
    }
}
