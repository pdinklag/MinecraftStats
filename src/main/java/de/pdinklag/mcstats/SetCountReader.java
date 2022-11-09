package de.pdinklag.mcstats;

import org.json.JSONArray;
import org.json.JSONObject;

public class SetCountReader extends JSONDataReader {
    public SetCountReader(String[] path) {
        super(path);
    }

    @Override
    protected DataValue getDefaultValue() {
        return new StringSetValue();
    }

    @Override
    protected DataValue read(JSONObject obj, String key) {
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
    public DataAggregator createDefaultAggregator() {
        return new StringSetMergeAggregator(); 
    }
}
