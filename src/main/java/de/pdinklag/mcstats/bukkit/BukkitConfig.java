package de.pdinklag.mcstats.bukkit;

import java.nio.file.Path;

import org.bukkit.Server;
import org.bukkit.configuration.Configuration;

import de.pdinklag.mcstats.Config;
import de.pdinklag.mcstats.FileSystemDataSource;

public class BukkitConfig extends Config {
    private static final String DEFAULT_WORLD_NAME= "world";

    private String subdirName = "stats";
    private boolean unpackWebFiles = true;
    private int updateInterval = 5;

    public BukkitConfig(Server server, Configuration bukkitConfig)  {
        // create data source
        getDataSources().add(new FileSystemDataSource(Path.of(server.getWorldContainer().getAbsolutePath()), DEFAULT_WORLD_NAME));

        // read config
        String documentRoot = bukkitConfig.getString("data.documentRoot");
        if(documentRoot != null) 
        {
            setDocumentRoot(Path.of(documentRoot));
        }

        subdirName = bukkitConfig.getString("data.subdirName", subdirName);
        unpackWebFiles = bukkitConfig.getBoolean("data.unpackWebFiles", unpackWebFiles);
        updateInterval = bukkitConfig.getInt("data.updateInterval", updateInterval);

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

    public String getSubdirName() {
        return subdirName;
    }

    public void setSubdirName(String subdirName) {
        this.subdirName = subdirName;
    }
    
    public boolean isUnpackWebFiles() {
        return unpackWebFiles;
    }

    public void setUnpackWebFiles(boolean unpackWebFiles) {
        this.unpackWebFiles = unpackWebFiles;
    }

    public int getUpdateInterval() {
        return updateInterval;
    }

    public void setUpdateInterval(int updateInterval) {
        this.updateInterval = updateInterval;
    }
}
