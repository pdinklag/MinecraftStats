package de.pdinklag.mcstats;

/**
 * Interface for aggregators of data values.
 */
public interface DataAggregator {
    /**
     * Aggregates two data values.
     * @param a the first data value
     * @param b the second data value
     * @return the aggregate value
     */
    public DataValue aggregate(DataValue a, DataValue b);
}
