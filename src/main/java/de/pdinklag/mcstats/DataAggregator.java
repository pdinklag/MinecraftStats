package de.pdinklag.mcstats;

public interface DataAggregator {
    public DataValue aggregate(DataValue a, DataValue b);
}
