package de.pdinklag.mcstats;

import org.json.JSONObject;

public interface IReader {
    public IValue read(JSONObject stats);

    public IAggregator createDefaultAggregator();
}
