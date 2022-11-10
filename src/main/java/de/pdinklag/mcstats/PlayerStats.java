package de.pdinklag.mcstats;

import java.util.HashMap;

import org.json.JSONObject;

/**
 * Holds a player's aggregated stats.
 */
public class PlayerStats {
    private final HashMap<Stat, DataValue> stats = new HashMap<>();

    /**
     * Constructs an empty player stats holder.
     */
    public PlayerStats() {
    }

    /**
     * Gathers data for the given stats and data held in the player's stat JSON.
     * If a data value already exists for some stat, it will be aggregated with the
     * new value.
     * 
     * @param stats the stats to consider
     * @param data  the data object to read from
     */
    public void gather(Iterable<Stat> stats, JSONObject data) {
        final int dataVersion = DefaultReaders.DATA_VERSION_READER.read(data).toInt();
        stats.forEach(stat -> {
            if (stat.isVersionSupported(dataVersion)) {
                setOrAggregate(stat, stat.getReader().read(data));
            }
        });
    }

    private void setOrAggregate(Stat stat, DataValue value) {
        if (stats.containsKey(stat)) {
            value = stat.getAggregator().aggregate(stats.get(stat), value);
        }
        stats.put(stat, value);
    }

    /**
     * Gets the data value for the given stat.
     * 
     * @param stat the stat in question
     * @return the data value for the given stat
     */
    public DataValue get(Stat stat) {
        return stats.getOrDefault(stat, new NoValue());
    }
}
