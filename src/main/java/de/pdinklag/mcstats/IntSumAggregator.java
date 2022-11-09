package de.pdinklag.mcstats;

/**
 * Aggregates two values by adding them together.
 */
public class IntSumAggregator implements DataAggregator {
    @Override
    public DataValue aggregate(DataValue a, DataValue b) {
        return new IntValue(a.toInt() + b.toInt());
    }
}
