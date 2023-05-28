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

            final Path jsonDir = jsonPath.toAbsolutePath().getParent();
            setEventsPath(jsonDir.resolve(data.optString("eventsDir", "events")));
            setStatsPath(jsonDir.resolve(data.optString("statsDir", "stats")));
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
        }

        // player settings
        final JSONObject players = json.optJSONObject("players");
        if (players != null) {
            setInactiveDays(players.optInt("inactiveDays", getInactiveDays()));
            setMinPlaytime(players.optInt("minPlaytime", getMinPlaytime()));
            setUpdateInactive(players.optBoolean("updateInactive", isUpdateInactive()));
            setProfileUpdateInterval(players.optInt("profileUpdateInterval", getProfileUpdateInterval()));

            setExcludeBanned(players.optBoolean("excludeBanned", isExcludeBanned()));
            setExcludeOps(players.optBoolean("excludeOps", isExcludeOps()));

            final JSONArray excludeUUIDs = players.optJSONArray("excludeUUIDs");
            if (excludeUUIDs != null) {
                for (int i = 0; i < excludeUUIDs.length(); i++) {
                    getExcludeUUIDs().add(excludeUUIDs.getString(i));
                }
            }
        }

        // crown settings
        final JSONObject crown = json.optJSONObject("crown");
        if(crown != null)
        {
            setGoldMedalWeight(crown.optInt("gold", getGoldMedalWeight()));
            setSilverMedalWeight(crown.optInt("silver", getSilverMedalWeight()));
            setBronzeMedalWeight(crown.optInt("bronze", getBronzeMedalWeight()));
        }

        // client settings
        final JSONObject client = json.optJSONObject("client");
        if(client != null)
        {
            setPlayersPerPage(client.optInt("playersPerPage", getPlayersPerPage()));
            setPlayerCacheUUIDPrefix(client.optInt("playerCacheUUIDPrefix", getPlayerCacheUUIDPrefix()));
            setDefaultLanguage(client.optString("defaultLanguage", getDefaultLanguage()));
            setServerName(client.optString("serverName", getServerName()));
            setShowLastOnline(client.optBoolean("showLastOnline", isShowLastOnline()));
        }
    }
}
