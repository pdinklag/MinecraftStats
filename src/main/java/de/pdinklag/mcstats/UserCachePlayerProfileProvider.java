package de.pdinklag.mcstats;

import java.util.HashMap;

import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Provides player profiles via the Minecraft server's usercache.json.
 * It can only provide names, not skins.
 */
public class UserCachePlayerProfileProvider implements PlayerProfileProvider {
    private final HashMap<String, String> uuidToName = new HashMap<>();

    /**
     * Constructs a usercache provider.
     * 
     * @param usercache the contents of usercache.json
     */
    public UserCachePlayerProfileProvider(JSONArray usercache) {
        for (int i = 0; i < usercache.length(); i++) {
            JSONObject entry = usercache.getJSONObject(i);
            if (entry.has("uuid") && entry.has("name")) {
                String u = entry.getString("uuid");
                String name = entry.getString("name");
                uuidToName.put(u.toLowerCase(), name);
                uuidToName.put(u.replace("-", "").toLowerCase(), name);
            }
        }
    }

    @Override
    public PlayerProfile getPlayerProfile(Player player) {
        String uuid = player.getUuid().toLowerCase();
        String cleanUuid = uuid.replace("-", "");
        if (uuidToName.containsKey(uuid)) {
            return new PlayerProfile(uuidToName.get(uuid));
        } else if (uuidToName.containsKey(cleanUuid)) {
            return new PlayerProfile(uuidToName.get(cleanUuid));
        } else {
            return player.getProfile();
        }
    }
}
