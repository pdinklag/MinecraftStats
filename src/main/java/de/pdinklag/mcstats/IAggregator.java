package de.pdinklag.mcstats;

public interface IAggregator<V extends IValue> {
    public V aggregate(V a, V b);
}
