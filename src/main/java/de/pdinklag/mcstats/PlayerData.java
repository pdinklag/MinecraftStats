package de.pdinklag.mcstats;

import java.util.HashMap;

import org.json.JSONObject;

public class PlayerData {
    private final HashMap<Stat, IValue> stats = new HashMap<>();

    public PlayerData() {
    }

    public void gather(JSONObject data, Iterable<Stat> stats) {
        stats.forEach(stat -> {
            setOrAggregate(stat, stat.getReader().read(data));
        });
    }

    private void setOrAggregate(Stat stat, IValue value) {
        if (stats.containsKey(stat)) {
            value = stat.getAggregator().aggregate(stats.get(stat), value);
        }
        stats.put(stat, value);
    }

    public IValue get(Stat stat) {
        return stats.getOrDefault(stat, new NoValue());
    }
}
