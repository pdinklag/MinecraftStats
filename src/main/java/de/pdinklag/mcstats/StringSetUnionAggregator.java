package de.pdinklag.mcstats;

/**
 * Aggregates two string sets by computing the union.
 */
public class StringSetUnionAggregator implements DataAggregator {
    @Override
    public StringSetValue aggregate(DataValue a, DataValue b) {
        StringSetValue merged = new StringSetValue();
        merged.addAll(((StringSetValue)a).getSet());
        merged.addAll(((StringSetValue)b).getSet());
        return merged;
    }
}
