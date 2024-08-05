package de.pdinklag.mcstats;

import org.json.JSONArray;
import org.json.JSONObject;

/**
 * A player filter that excludes players stated in a JSON file (such as
 * banned-players.json or ops.json).
 */
public class JSONPlayerFilter extends ExcludeUUIDPlayerFilter {
    private final String criteria;

    /**
     * Constructs a filter.
     * 
     * @param excludedPlayers the JSON array of information objects for players to
     *                        exclude
     */
    public JSONPlayerFilter(JSONArray excludedPlayers, String criteria) {
        this.criteria = criteria;
        for (int i = 0; i < excludedPlayers.length(); i++) {
            JSONObject entry = excludedPlayers.getJSONObject(i);
            exclude(entry.getString("uuid"));
        }
    }

    @Override
    public String getFilterCriteria() {
        return criteria;
    }
}
