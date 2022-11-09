package de.pdinklag.mcstats;

import org.json.JSONObject;

public class IntReader extends JSONDataReader {
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
