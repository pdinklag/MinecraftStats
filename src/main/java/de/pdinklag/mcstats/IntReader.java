package de.pdinklag.mcstats;

import org.json.JSONObject;

public class IntReader extends JSONReader {
    public IntReader(String[] path) {
        super(path);
    }

    @Override
    protected IValue read(JSONObject obj, String key) {
        return new IntValue(obj.optInt(key, 0));
    }

    @Override
    protected IValue getDefaultValue() {
        return new IntValue(0);
    }

    @Override
    public IAggregator createDefaultAggregator() {
        return new IntSumAggregator();
    }
}
