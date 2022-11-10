package de.pdinklag.mcstats;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * Provides player profiles from the previous update's database (players.json).
 */
public class DatabasePlayerProfileProvider implements PlayerProfileProvider {
    private JSONObject playersJson;

    /**
     * Constructs a database profile provider.
     * 
     * @param playersJson the contents of players.json
     */
    public DatabasePlayerProfileProvider(JSONObject playersJson) {
        this.playersJson = playersJson;
    }

    @Override
    public PlayerProfile getPlayerProfile(Player player) {
        if (playersJson.has(player.getUuid())) {
            try {
                JSONObject obj = playersJson.getJSONObject(player.getUuid());
                return new PlayerProfile(
                    obj.getString("name"),
                    obj.getString("skin"),
                    obj.getLong("update"));
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
        return player.getProfile();
    }
}
