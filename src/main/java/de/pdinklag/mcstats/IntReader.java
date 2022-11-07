package de.pdinklag.mcstats;

import org.json.JSONObject;

public class IntReader extends JSONReader<IntValue> {
    public IntReader(String[] path) {
        super(path);
    }

    @Override
    protected IntValue read(JSONObject obj, String key) {
        return new IntValue(obj.optInt(key, 0));
    }

    @Override
    protected IntValue getDefaultValue() {
        return new IntValue(0);
    }
}
