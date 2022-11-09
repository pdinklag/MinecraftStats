package de.pdinklag.mcstats;

import org.json.JSONObject;

public abstract class JSONDataReader implements DataReader {
    private final String[] path;

    protected JSONDataReader(String[] path) {
        this.path = path;
    }

    protected abstract DataValue getDefaultValue();

    protected abstract DataValue read(JSONObject obj, String key);

    public DataValue read(JSONObject stats) {
        final int depth = path.length - 1;
        for(int i = 0; i < depth; i++)
        {
            stats = stats.optJSONObject(path[i]);
            if(stats == null) return getDefaultValue();
        }
        return read(stats, path[depth]);
    }
}
