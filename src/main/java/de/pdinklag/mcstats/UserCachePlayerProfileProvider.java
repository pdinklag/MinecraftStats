package de.pdinklag.mcstats;

import java.util.HashMap;

import org.json.JSONArray;
import org.json.JSONObject;

public class UserCachePlayerProfileProvider implements PlayerProfileProvider {
    private final HashMap<String, String> uuidToName = new HashMap<>();

    public UserCachePlayerProfileProvider(JSONArray usercache) {
        for(int i = 0; i < usercache.length(); i++) {
            JSONObject entry = usercache.getJSONObject(i);
            uuidToName.put(entry.getString("uuid"), entry.getString("name"));
        }
    }

    @Override
    public PlayerProfile getPlayerProfile(Player player) {
        String uuid = player.getUuid();
        if(uuidToName.containsKey(uuid)) {
            return new PlayerProfile(uuidToName.get(uuid), null);
        } else {
            return player.getProfile();
        }
    }
}
