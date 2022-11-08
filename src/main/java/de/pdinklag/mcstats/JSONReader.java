package de.pdinklag.mcstats;

import org.json.JSONObject;

public abstract class JSONReader implements IReader {
    private final String[] path;

    protected JSONReader(String[] path) {
        this.path = path;
    }

    protected abstract IValue getDefaultValue();

    protected abstract IValue read(JSONObject obj, String key);

    public IValue read(JSONObject stats) {
        final int depth = path.length - 1;
        for(int i = 0; i < depth; i++)
        {
            stats = stats.optJSONObject(path[i]);
            if(stats == null) return getDefaultValue();
        }
        return read(stats, path[depth]);
    }
}
