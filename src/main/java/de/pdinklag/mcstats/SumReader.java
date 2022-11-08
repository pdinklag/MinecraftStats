package de.pdinklag.mcstats;

import org.json.JSONObject;

public class SumReader implements IReader {
    private final IReader[] readers;

    public SumReader(IReader[] readers) {
        this.readers = readers;
    }

    @Override
    public IValue read(JSONObject stats) {
        int sum = 0;
        for (IReader r : readers) {
            sum += r.read(stats).toInt();
        }
        return new IntValue(sum);
    }

    @Override
    public IAggregator createDefaultAggregator() {
        return new IntSumAggregator();
    }
}
