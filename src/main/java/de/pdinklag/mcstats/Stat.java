package de.pdinklag.mcstats;

/**
 * Represents a MinecraftStats stat.
 */
public class Stat {
    /**
     * The unit in which scores are measured in.
     */
    public enum Unit {
        /**
         * Generic integers, typically denoting a count.
         */
        INT,

        /**
         * Centimeters, Minecraft's default unit to measure distances.
         */
        CM,

        /**
         * Ticks, Minecraft's default unit to measure durations (with typically 20 ticks per second).
         */
        TICKS,

        /**
         * Tenths of a heart, Minecraft's default unit to measure health and damage.
         */
        TENTHS_OF_HEART;

        @Override
        public String toString() {
            return name().toLowerCase();
        }
    }

    private final String id;
    private final Unit unit;
    private final int minVersion;
    private final int maxVersion;
    private final DataReader reader;
    private final DataAggregator aggregator;

    /**
     * Constructs a stat.
     * @param id the stat's identifier
     * @param unit the unit in which the stat score is measured
     * @param minVersion the minimum Minecraft version (data value) for which the stat is supported
     * @param maxVersion the maximum Minecraft version (data value) for which the stat is supported
     * @param reader the data value reader
     * @param aggregator the data value aggregator
     */
    public Stat(String id, Unit unit, int minVersion, int maxVersion, DataReader reader, DataAggregator aggregator) {
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

    public boolean isVersionSupported(int dataVersion) {
        return dataVersion >= minVersion && dataVersion <= maxVersion;
    }

    public DataReader getReader() {
        return reader;
    }

    public DataAggregator getAggregator() {
        return aggregator;
    }
}
