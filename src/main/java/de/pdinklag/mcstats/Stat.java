package de.pdinklag.mcstats;

import org.json.JSONObject;

public class Stat<V extends IValue> {
    public enum Unit {
        NUMBER("int"),
        DISTANCE("cm"),
        DURATION("ticks"),
        HEALTH("tenths_of_heart");

        private final String code;

        private Unit(String code) {
            this.code = code;
        }

        @Override
        public String toString() {
            return code;
        }
    }

    private String name;
    private Unit unit;
    private IReader<V> reader;
    private IAggregator<V> aggregator;
    private int minVersion;
    private int maxVersion;

    public String getName() {
        return name;
    }

    public Unit getUnit() {
        return unit;
    }

    public boolean isEligible(int version) {
        return version >= minVersion && version <= maxVersion;
    }

    @SuppressWarnings("unchecked")
    public V aggregate(IValue a, IValue b) {
        return aggregator.aggregate((V)a, (V)b);
    }

    public V read(JSONObject stats) {
        return reader.read(stats);
    }
}
