package de.pdinklag.mcstats;

import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeParseException;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * Provides functionality to parse event definitions from JSON.
 */
public class EventParser {
    private static String complyISO8601(String s) {
        // even though ISO 8601 allows a space used in place of a T, the Java parser does not accept that
        return s.replace(' ', 'T');
    }

    private static long parseISO8601(String s) {
        return LocalDateTime.parse(complyISO8601(s)).atZone(ZoneId.systemDefault()).toInstant().toEpochMilli();
    }

    /**
     * Parses a JSON object into an event definiton.
     * @param obj the JSON object to parse
     * @return the resulting event
     * @throws EventParseException in case an error occurs trying to parse the object
     */
    public static Event parse(JSONObject obj) throws EventParseException {
        try {
            final String id = obj.getString("name");
            final String title = obj.getString("title");
            final String linkedStatId = obj.getString("stat");
            final long startTime = parseISO8601(obj.getString("startTime"));
            final long endTime = parseISO8601(obj.getString("endTime"));

            if(startTime >= endTime) {
                throw new EventParseException("event ends before it starts: " + id);
            }

            return new Event(id, title, startTime, endTime, linkedStatId);
        } catch(DateTimeParseException  e) {
            throw new EventParseException(e);
        } catch(JSONException e) {
            throw new EventParseException(e);
        }
    }
}
