package de.pdinklag.mcstats;

import org.json.JSONObject;

public abstract class JSONReader<V extends IValue> implements IReader<V> {
    private final String[] path;

    protected JSONReader(String[] path) {
        this.path = path;
    }

    protected abstract V getDefaultValue();

    protected abstract V read(JSONObject obj, String key);

    @Override
    public V read(JSONObject stats) {
        final int depth = path.length - 1;
        for(int i = 0; i < depth; i++)
        {
            stats = stats.optJSONObject(path[i]);
            if(stats == null) return getDefaultValue();
        }
        return read(stats, path[depth]);
    }
}
