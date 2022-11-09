package de.pdinklag.mcstats;

import org.json.JSONObject;

public class SumReader implements DataReader {
    private final DataReader[] readers;

    public SumReader(DataReader[] readers) {
        this.readers = readers;
    }

    @Override
    public DataValue read(JSONObject stats) {
        int sum = 0;
        for (DataReader r : readers) {
            sum += r.read(stats).toInt();
        }
        return new IntValue(sum);
    }

    @Override
    public DataAggregator createDefaultAggregator() {
        return new IntSumAggregator();
    }
}
