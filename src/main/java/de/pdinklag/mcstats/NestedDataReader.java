package de.pdinklag.mcstats;

import org.json.JSONObject;

/**
 * Abstract base for data readers that read a value from a nested object.
 */
public abstract class NestedDataReader implements DataReader {
    private final String[] path;

    protected NestedDataReader(String[] path) {
        this.path = path;
    }

    protected abstract DataValue getDefaultValue();

    protected abstract DataValue read(JSONObject obj, String key);

    @Override
    public DataValue read(JSONObject stats) {
        final int depth = path.length - 1;
        for (int i = 0; i < depth; i++) {
            stats = stats.optJSONObject(path[i]);
            if (stats == null) {
                return getDefaultValue();
            }
        }
        return read(stats, path[depth]);
    }
}
