package de.pdinklag.mcstats;

import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Reads a set of strings.
 */
public class SetCountReader extends NestedDataReader {
    /**
     * Constructs a set count reader
     * @param path the JSON object names on the path to the set to read
     */
    public SetCountReader(String[] path) {
        super(path);
    }

    @Override
    protected DataValue getDefaultValue() {
        return new StringSetValue();
    }

    @Override
    protected DataValue read(JSONObject obj, String key) {
        final StringSetValue set = new StringSetValue();

        final JSONObject sub = obj.optJSONObject(key);
        if(sub != null) {
            sub.keySet().forEach(x -> {
                set.add(x);
            });
        } else {
            final JSONArray array = obj.optJSONArray(key);
            if (array != null) {
                array.forEach(x -> {
                    set.add(x.toString());
                });
            }
        }
        return set;
    }

    @Override
    public DataAggregator createDefaultAggregator() {
        return new StringSetUnionAggregator(); 
    }
}
