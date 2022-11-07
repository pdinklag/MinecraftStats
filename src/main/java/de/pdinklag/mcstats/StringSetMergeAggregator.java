package de.pdinklag.mcstats;

public class StringSetMergeAggregator implements IAggregator<StringSetValue> {
    @Override
    public StringSetValue aggregate(StringSetValue a, StringSetValue b) {
        StringSetValue merged = new StringSetValue();
        merged.addAll(a.getSet());
        merged.addAll(b.getSet());
        return merged;
    }
    
}
