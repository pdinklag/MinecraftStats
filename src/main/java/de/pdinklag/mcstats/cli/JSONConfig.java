package de.pdinklag.mcstats.cli;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import de.pdinklag.mcstats.Config;
import de.pdinklag.mcstats.FileSystemDataSource;

public class JSONConfig extends Config {
    public JSONConfig(Path jsonPath) throws IOException, JSONException {
        final JSONObject json = new JSONObject(Files.readString(jsonPath));

        // data settings
        {
            final JSONObject data = json.getJSONObject("data");
            setDocumentRoot(Path.of(data.getString("documentRoot")));
            setEventsPath(jsonPath.resolve(data.getString("eventsDir")));
            setStatsPath(jsonPath.resolve(data.getString("statsDir")));
        }

        // server settings
        {
            final JSONObject server = json.getJSONObject("server");
            final JSONArray sources = server.getJSONArray("sources");
            for (int i = 0; i < sources.length(); i++) {
                JSONObject source = sources.getJSONObject(i);
                getDataSources().add(new FileSystemDataSource(
                        Path.of(source.getString("path")),
                        source.getString("worldName")));
            }
            setCustomName(server.optString("customName", null));
        }

        // player settings
        {
            final JSONObject players = json.getJSONObject("players");
            setInactiveDays(players.getInt("inactiveDays"));
            setMinPlaytime(players.getInt("minPlaytime"));
            setUpdateInactive(players.getBoolean("updateInactive"));
            setProfileUpdateInterval(players.getInt("profileUpdateInterval"));
            setShowLastOnline(players.getBoolean("showLastOnline"));

            setExcludeBanned(players.getBoolean("excludeBanned"));
            setExcludeOps(players.getBoolean("excludeOps"));

            final JSONArray excludeUUIDs = players.getJSONArray("excludeUUIDs");
            for (int i = 0; i < excludeUUIDs.length(); i++) {
                getExcludeUUIDs().add(excludeUUIDs.getString(i));
            }
        }

        // crown settings
        {
            final JSONObject crown = json.getJSONObject("crown");
            setGoldMedalWeight(crown.getInt("gold"));
            setSilverMedalWeight(crown.getInt("silver"));
            setBronzeMedalWeight(crown.getInt("bronze"));
        }

        // client settings
        {
            final JSONObject client = json.getJSONObject("client");
            setPlayersPerPage(client.getInt("playersPerPage"));
            setPlayerCacheUUIDPrefix(client.getInt("playerCacheUUIDPrefix"));
            setDefaultLanguage(client.getString("defaultLanguage"));
        }
    }
}
