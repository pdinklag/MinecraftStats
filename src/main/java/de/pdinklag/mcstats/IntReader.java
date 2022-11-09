package de.pdinklag.mcstats;

import org.json.JSONObject;

/**
 * Reads a single integer value from a nested object.
 */
public class IntReader extends NestedDataReader {
    /**
     * Constructs an integer reader
     * @param path the JSON object names on the path to the value to read
     */
    public IntReader(String[] path) {
        super(path);
    }

    @Override
    protected DataValue read(JSONObject obj, String key) {
        return new IntValue(obj.optInt(key, 0));
    }

    @Override
    protected DataValue getDefaultValue() {
        return new IntValue(0);
    }

    @Override
    public DataAggregator createDefaultAggregator() {
        return new IntSumAggregator();
    }
}
