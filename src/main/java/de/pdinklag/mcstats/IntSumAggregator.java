package de.pdinklag.mcstats;

public class IntSumAggregator implements IAggregator<IntValue> {
    @Override
    public IntValue aggregate(IntValue a, IntValue b) {
        return new IntValue(a.toInt() + b.toInt());
    }
}
