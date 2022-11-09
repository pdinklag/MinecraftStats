package de.pdinklag.mcstats;

public class IntSumAggregator implements DataAggregator {
    public DataValue aggregate(DataValue a, DataValue b) {
        return new IntValue(a.toInt() + b.toInt());
    }
}
