package de.pdinklag.mcstats;

import org.json.JSONObject;

public interface IReader<V extends IValue> {
    public V read(JSONObject stats);
}
