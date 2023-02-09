package de.pdinklag.mcstats.cli;

import java.nio.file.Path;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import de.pdinklag.mcstats.Config;
import de.pdinklag.mcstats.FileSystemDataSource;

public class JSONConfig extends Config {
    public JSONConfig() {
    }
    
    public JSONConfig(JSONObject json) throws JSONException {
        // read databaseDir
        setDatabasePath(Path.of(json.optString("databaseDir")));

        // read data sources
        {
            JSONObject server = json.getJSONObject("server");
            JSONArray sources = server.getJSONArray("sources");
            for(int i = 0; i < sources.length(); i++) {
                JSONObject source = sources.getJSONObject(i);
                getDataSources().add(new FileSystemDataSource(
                    Path.of(source.getString("path")), 
                    source.getString("worldName")));
            }
        }

        // player settings
        {
            JSONObject players = json.getJSONObject("players");
            setInactiveDays(players.getInt("inactiveDays"));
            setMinPlaytime(players.getInt("minPlaytime"));
            setUpdateInactive(players.getBoolean("updateInactive"));
            setProfileUpdateInterval(players.getInt("profileUpdateInterval"));

            setExcludeBanned(players.getBoolean("excludeBanned"));
            setExcludeOps(players.getBoolean("excludeOps"));

            JSONArray excludeUUIDs = players.getJSONArray("excludeUUIDs");
            for(int i = 0; i< excludeUUIDs.length(); i++) {
                getExcludeUUIDs().add(excludeUUIDs.getString(i));
            }
        }
    }
}
