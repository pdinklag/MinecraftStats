package de.pdinklag.mcstats;

import org.json.JSONObject;

public class SumReader implements IReader<IntValue> {
    private final IReader<?>[] readers;

    public SumReader(IReader<?>[] readers) {
        this.readers = readers;
    }

    @Override
    public IntValue read(JSONObject stats) {
        int sum = 0;
        for (IReader<?> r : readers) {
            sum += r.read(stats).toInt();
        }
        return new IntValue(sum);
    }
}
