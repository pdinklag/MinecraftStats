package de.pdinklag.mcstats;

import java.util.HashMap;

import org.json.JSONObject;

/**
 * Holds a player's aggregated stats.
 */
public class PlayerStats {
    private final HashMap<Stat, DataValue> stats = new HashMap<>();
    private final HashMap<Stat, Integer> statRanks = new HashMap<>();

    private int goldMedals = 0;
    private int silverMedals = 0;
    private int bronzeMedals = 0;

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
     * If applicable, also counts the corresponding medal.
     * 
     * @param stat the stat in question
     * @param rank the player's rank for the stat
     */
    public void setRank(Stat stat, int rank) {
        switch (rank) {
            case 1:
                ++goldMedals;
                break;

            case 2:
                ++silverMedals;
                break;

            case 3:
                ++bronzeMedals;
                break;
        }
        statRanks.put(stat, rank);
    }

    /**
     * Gets the player's crown score for the given parameters.
     * 
     * @param goldWeight the weight of a gold medal
     * @param silverWeight the weight of a silver medal
     * @param bronzeWeight the weight of a bronze medal
     * @return the crown score according to the weights
     */
    public int getCrownScore(int goldWeight, int silverWeight, int bronzeWeight) {
        return goldMedals * goldWeight + silverMedals * silverWeight + bronzeMedals * bronzeWeight;
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
