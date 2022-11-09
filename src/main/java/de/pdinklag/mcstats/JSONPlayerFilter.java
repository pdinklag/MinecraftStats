package de.pdinklag.mcstats;

import java.util.HashSet;

import org.json.JSONArray;
import org.json.JSONObject;

/**
 * A player filter that excludes players stated in a JSON file (such as banned-players.json or ops.json).
 */
public class JSONPlayerFilter implements PlayerFilter {
    private final HashSet<String> excludedUuids = new HashSet<>();

    /**
     * Constructs a filter.
     * @param excludedPlayers the JSON array of information objects for players to exclude
     */
    public JSONPlayerFilter(JSONArray excludedPlayers) {
        for(int i = 0; i < excludedPlayers.length(); i++) {
            JSONObject entry = excludedPlayers.getJSONObject(i);
            excludedPlayers.put(entry.getString("uuid"));
        }
    }

    @Override
    public boolean filter(Player player) {
        return !excludedUuids.contains(player.getUuid());
    }
}
