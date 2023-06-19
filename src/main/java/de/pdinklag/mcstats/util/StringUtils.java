package de.pdinklag.mcstats.util;

/**
 * Utilities related to strings.
 */
public class StringUtils {
    /**
     * Encodes the given string as ASCII by escaping all non-ASCII characters.
     * @param s the input string
     * @return the encoded string
     */
    public static String encodeASCII(String s) {
        final StringBuilder sb = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            final char c = s.charAt(i);
            if (c <= 127) {
                sb.append(c);
            }
            else {
                sb.append("\\u").append(String.format("%04x", (int)c));
            } 
        }
        return sb.toString();
    }
}
