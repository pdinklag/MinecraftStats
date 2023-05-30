package de.pdinklag.mcstats;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * Provides player profiles from the previous update's database (players.json).
 */
public class DatabasePlayerProfileProvider implements PlayerProfileProvider {
    public static JSONObject createDatabase(Iterable<Player> players) {
        JSONObject db = new JSONObject();
        players.forEach(player -> {
            PlayerProfile profile = player.getProfile();
            if (profile.hasName()) {
                JSONObject obj = new JSONObject();
                obj.put("name", profile.getName());
                obj.put("skin", profile.getSkin());
                obj.put("update", profile.getLastUpdateTime());
                db.put(player.getUuid(), obj);
            }
        });
        return db;
    }

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
                final JSONObject obj = playersJson.getJSONObject(player.getUuid());
                final String name = obj.getString("name");
                if (!player.getUuid().equals(name)) {
                    return new PlayerProfile(
                            name,
                            obj.optString("skin", null),
                            obj.getLong("update"));
                }
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
        return player.getProfile();
    }
}
