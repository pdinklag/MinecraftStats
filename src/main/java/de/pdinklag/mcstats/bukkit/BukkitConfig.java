package de.pdinklag.mcstats.bukkit;

import java.nio.file.Path;

import org.bukkit.Server;
import org.bukkit.configuration.Configuration;

import de.pdinklag.mcstats.Config;
import de.pdinklag.mcstats.FileSystemDataSource;

public class BukkitConfig extends Config {
    private static final String DEFAULT_WORLD_NAME= "world";

    private int updateInterval = 5;

    public BukkitConfig(Server server, Configuration bukkitConfig)  {
        // create data source
        getDataSources().add(new FileSystemDataSource(Path.of(server.getWorldContainer().getAbsolutePath()), DEFAULT_WORLD_NAME));

        // read config
        String databaseDir = bukkitConfig.getString("server.databaseDir");
        if(databaseDir != null) 
        {
            setDatabasePath(Path.of(databaseDir));
        }

        updateInterval = bukkitConfig.getInt("updateInterval", updateInterval);

        setCustomName(bukkitConfig.getString("server.customName", getCustomName()));

        setInactiveDays(bukkitConfig.getInt("players.inactiveDays", getInactiveDays()));
        setMinPlaytime(bukkitConfig.getInt("players.minPlaytime", getMinPlaytime()));
        setUpdateInactive(bukkitConfig.getBoolean("players.updateInactive", isUpdateInactive()));
        setProfileUpdateInterval(bukkitConfig.getInt("players.profileUpdateInterval", getProfileUpdateInterval()));
        setShowLastOnline(bukkitConfig.getBoolean("players.showLastOnline", isShowLastOnline()));

        setExcludeBanned(bukkitConfig.getBoolean("players.excludeBanned", isExcludeBanned()));
        setExcludeOps(bukkitConfig.getBoolean("players.excludeOps", isExcludeOps()));
        
        getExcludeUUIDs().addAll(bukkitConfig.getStringList("players.excludeUUIDs"));

        setBronzeMedalWeight(bukkitConfig.getInt("crown.bronze", getBronzeMedalWeight()));
        setSilverMedalWeight(bukkitConfig.getInt("crown.silver", getSilverMedalWeight()));
        setGoldMedalWeight(bukkitConfig.getInt("crown.gold", getGoldMedalWeight()));

        setDefaultLanguage(bukkitConfig.getString("client.defaultLanguage", getDefaultLanguage()));
        setPlayersPerPage(bukkitConfig.getInt("client.playersPerPage", getPlayersPerPage()));
        setPlayerCacheUUIDPrefix(bukkitConfig.getInt("client.playerCacheUUIDPrefix", getPlayerCacheUUIDPrefix()));
    }

    public int getUpdateInterval() {
        return updateInterval;
    }

    public void setUpdateInterval(int updateInterval) {
        this.updateInterval = updateInterval;
    }
}
