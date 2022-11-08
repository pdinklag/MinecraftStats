package de.pdinklag.mcstats;

public class Stat {
    public enum Unit {
        INT, CM, TICKS, TENTHS_OF_HEART;

        @Override
        public String toString() {
            return name().toLowerCase();
        }
    }

    private final String id;
    private final Unit unit;
    private final int minVersion;
    private final int maxVersion;
    private final IReader reader;
    private final IAggregator aggregator;

    public Stat(String id, Unit unit, int minVersion, int maxVersion, IReader reader, IAggregator aggregator) {
        this.id = id;
        this.unit = unit;
        this.minVersion = minVersion;
        this.maxVersion = maxVersion;
        this.reader = reader;
        this.aggregator = aggregator;
    }

    public String getId() {
        return id;
    }

    public Unit getUnit() {
        return unit;
    }

    public boolean isEligible(int version) {
        return version >= minVersion && version <= maxVersion;
    }

    public IReader getReader() {
        return reader;
    }

    public IAggregator getAggregator() {
        return aggregator;
    }
}
