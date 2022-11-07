package de.pdinklag.mcstats;

import org.json.JSONArray;
import org.json.JSONObject;

public class StringSetReader extends JSONReader<StringSetValue> {
    public StringSetReader(String... path) {
        super(path);
    }

    @Override
    protected StringSetValue getDefaultValue() {
        return new StringSetValue();
    }

    @Override
    protected StringSetValue read(JSONObject obj, String key) {
        StringSetValue set = new StringSetValue();
        JSONArray array = obj.optJSONArray(key);
        if (array != null) {
            array.forEach(x -> {
                set.add(x.toString());
            });
        }
        return set;
    }
}
