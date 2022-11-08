package de.pdinklag.mcstats;

public class StringSetMergeAggregator implements IAggregator {
    public StringSetValue aggregate(IValue a, IValue b) {
        StringSetValue merged = new StringSetValue();
        merged.addAll(((StringSetValue)a).getSet());
        merged.addAll(((StringSetValue)b).getSet());
        return merged;
    }
}
