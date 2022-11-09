package de.pdinklag.mcstats;

import java.util.HashSet;

import org.json.JSONArray;
import org.json.JSONObject;

public class JSONPlayerFilter implements PlayerFilter {
    private final HashSet<String> excludedUuids = new HashSet<>();

    public JSONPlayerFilter(JSONArray bannedPlayers) {
        for(int i = 0; i < bannedPlayers.length(); i++) {
            JSONObject entry = bannedPlayers.getJSONObject(i);
            bannedPlayers.put(entry.getString("uuid"));
        }
    }

    @Override
    public boolean filter(Player player) {
        return !excludedUuids.contains(player.getUuid());
    }
}
