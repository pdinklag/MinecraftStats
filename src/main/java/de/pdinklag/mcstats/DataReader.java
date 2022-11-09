package de.pdinklag.mcstats;

import org.json.JSONObject;

public interface DataReader {
    public DataValue read(JSONObject stats);

    public DataAggregator createDefaultAggregator();
}
