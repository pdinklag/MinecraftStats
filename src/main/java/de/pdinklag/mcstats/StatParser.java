package de.pdinklag.mcstats;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

/**
 * Provides functionality to parse stat definitions from JSON.
 */
public class StatParser {
    private static IntReader parseIntReader(JSONObject obj) throws JSONException {
        JSONArray jsonPath = obj.getJSONArray("path");
        String[] path = new String[jsonPath.length()];
        for(int i = 0; i < path.length; i++) {
            path[i] = jsonPath.getString(i);
        }
        return new IntReader(path);
    }

    private static SumReader parseSumReader(JSONObject obj) throws JSONException {
        JSONArray jsonReaders = obj.getJSONArray("readers");
        DataReader[] readers = new DataReader[jsonReaders.length()];
        for(int i = 0; i < readers.length; i++) {
            readers[i] = parseReader(jsonReaders.getJSONObject(i));
        }
        return new SumReader(readers);
    }

    private static MatchSumReader parseMatchSumReader(JSONObject obj) throws JSONException {
        JSONArray jsonPath = obj.getJSONArray("path");
        String[] path = new String[jsonPath.length()];
        for(int i = 0; i < path.length; i++) {
            path[i] = jsonPath.getString(i);
        }

        JSONArray jsonPatterns = obj.getJSONArray("patterns");
        String[] patterns = new String[jsonPatterns.length()];
        for(int i = 0; i < patterns.length; i++) {
            patterns[i] = jsonPatterns.getString(i);
        }
        return new MatchSumReader(path, patterns);
    }

    private static SetCountReader parseSetCountReader(JSONObject obj) throws JSONException {
        JSONArray jsonPath = obj.getJSONArray("path");
        String[] path = new String[jsonPath.length()];
        for(int i = 0; i < path.length; i++) {
            path[i] = jsonPath.getString(i);
        }
        return new SetCountReader(path);
    }

    private static DataReader parseReader(JSONObject obj) throws JSONException, StatParseException {
        String type = obj.getString("$type");
        switch(type) {
            case "int":
                return parseIntReader(obj);
            case "sum":
                return parseSumReader(obj);
            case "match-sum":
                return parseMatchSumReader(obj);
            case "set-count":
                return parseSetCountReader(obj);
            default:
                throw new StatParseException("unsupported reader type: " + type);
        }
    }

    /**
     * Parses a JSON object into a stat definiton.
     * @param obj the JSON object to parse
     * @return the resulting stat
     * @throws StatParseException in case an error occurs trying to parse the object
     */
    public static Stat parse(JSONObject obj) throws StatParseException {
        try {
            final String id = obj.getString("id");
            final Stat.Unit unit = Stat.Unit.valueOf(obj.getString("unit").toUpperCase());
            final int minVersion = obj.optInt("minVersion", 0);
            final int maxVersion = obj.optInt("maxVersion", Integer.MAX_VALUE);
            final DataReader reader = parseReader(obj.getJSONObject("reader"));
            final DataAggregator aggregator = reader.createDefaultAggregator();
            return new Stat(id ,unit, minVersion, maxVersion, reader, aggregator);
        } catch(JSONException e) {
            throw new StatParseException(e);
        }
    }
}
