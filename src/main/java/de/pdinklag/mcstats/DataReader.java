package de.pdinklag.mcstats;

import org.json.JSONObject;

/**
 * Interface for data readers.
 */
public interface DataReader {
    /**
     * Reads a data value from the given JSON object.
     * @param stats the JSON objects to read from
     * @return the read data value
     */
    public DataValue read(JSONObject stats);

    /**
     * Creates an aggregator for read data values.
     * @return an aggregator for read data values
     */
    public DataAggregator createDefaultAggregator();
}
