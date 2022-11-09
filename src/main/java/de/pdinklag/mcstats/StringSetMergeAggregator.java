package de.pdinklag.mcstats;

public class StringSetMergeAggregator implements DataAggregator {
    public StringSetValue aggregate(DataValue a, DataValue b) {
        StringSetValue merged = new StringSetValue();
        merged.addAll(((StringSetValue)a).getSet());
        merged.addAll(((StringSetValue)b).getSet());
        return merged;
    }
}
