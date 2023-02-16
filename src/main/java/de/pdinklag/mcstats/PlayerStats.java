package de.pdinklag.mcstats;

import java.util.HashMap;

import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Holds a player's aggregated stats.
 */
public class PlayerStats {
    private final HashMap<Stat, DataValue> stats = new HashMap<>();
    private final HashMap<Stat, Integer> statRanks = new HashMap<>();

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
    public void gather(Iterable<Stat> stats, JSONObject data, int dataVersion) {
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

    /**
     * Sets the player's ranking for the given stat.
     * 
     * @param stat the stat in question
     * @param rank the player's rank for the stat
     */
    public void setRank(Stat stat, int rank) {
        // TODO: handle meta stats / crown score ranking here
        statRanks.put(stat, rank);
    }

    /**
     * Gets the player's stats report in JSON format.
     * 
     * @return the player's stats report in JSON format
     */
    public JSONObject toJSON() {
        JSONObject obj = new JSONObject();
        stats.forEach((stat, value) -> {
            JSONObject statData = new JSONObject();
            statData.put("value", value.toInt());
            if (statRanks.containsKey(stat)) {
                statData.put("rank", (int) statRanks.get(stat));
            }
            obj.put(stat.getId(), statData);
        });
        return obj;
    }
}
