package de.pdinklag.mcstats.util;

import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Utilities related to JSON.
 */
public class JSONUtils {
    /**
     * Encodes the given JSON object to an ASCII string.
     * @param obj the object to encode
     * @return the ASCII string representation
     */
    public static String toASCIIString(JSONObject obj) {
        return StringUtils.encodeASCII(obj.toString());
    }

    /**
     * Encodes the given JSON array to an ASCII string.
     * @param array the array to encode
     * @return the ASCII string representation
     */
    public static String toASCIIString(JSONArray array) {
        return StringUtils.encodeASCII(array.toString());
    }
}
