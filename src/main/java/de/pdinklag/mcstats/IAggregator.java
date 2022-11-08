package de.pdinklag.mcstats;

public interface IAggregator {
    public IValue aggregate(IValue a, IValue b);
}
