package de.pdinklag.mcstats;

public class IntSumAggregator implements IAggregator {
    public IValue aggregate(IValue a, IValue b) {
        return new IntValue(a.toInt() + b.toInt());
    }
}
