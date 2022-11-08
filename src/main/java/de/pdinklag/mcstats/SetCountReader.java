package de.pdinklag.mcstats;

import org.json.JSONArray;
import org.json.JSONObject;

public class SetCountReader extends JSONReader {
    public SetCountReader(String[] path) {
        super(path);
    }

    @Override
    protected IValue getDefaultValue() {
        return new StringSetValue();
    }

    @Override
    protected IValue read(JSONObject obj, String key) {
        StringSetValue set = new StringSetValue();
        JSONArray array = obj.optJSONArray(key);
        if (array != null) {
            array.forEach(x -> {
                set.add(x.toString());
            });
        }
        return set;
    }

    @Override
    public IAggregator createDefaultAggregator() {
        return new StringSetMergeAggregator(); 
    }
}
