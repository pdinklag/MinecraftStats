package de.pdinklag.mcstats.bukkit;

import java.nio.file.Path;

import org.bukkit.configuration.Configuration;
import org.bukkit.plugin.Plugin;

import de.pdinklag.mcstats.Config;
import de.pdinklag.mcstats.FileSystemDataSource;

public class BukkitConfig extends Config {
    private boolean unpackWebFiles = true;
    private int updateInterval = 5;
    private String webSubdir = "stats";
    private boolean skinsRestorerEnabled = false;

    public BukkitConfig(Plugin plugin)  {
        // create data source for default world
        final String defaultWorldName = plugin.getServer().getWorlds().get(0).getName();
        getDataSources().add(new FileSystemDataSource(Path.of(plugin.getServer().getWorldContainer().getAbsolutePath()), defaultWorldName));

        // read config
        final Configuration bukkitConfig = plugin.getConfig();
        String documentRoot = bukkitConfig.getString("data.documentRoot");
        if(documentRoot != null) 
        {
            setDocumentRoot(Path.of(documentRoot));
        }

        unpackWebFiles = bukkitConfig.getBoolean("data.unpackWebFiles", unpackWebFiles);
        updateInterval = bukkitConfig.getInt("data.updateInterval", updateInterval);
        webSubdir = bukkitConfig.getString("data.webSubdir", webSubdir);

        skinsRestorerEnabled = bukkitConfig.getBoolean("plugin.skinsRestorerEnabled", skinsRestorerEnabled);

        final Path pluginDataPath = plugin.getDataFolder().toPath();
        setEventsPath(pluginDataPath.resolve(bukkitConfig.getString("data.eventsDir")));
        setStatsPath(pluginDataPath.resolve(bukkitConfig.getString("data.statsDir")));
        setLogfilePath(pluginDataPath.resolve(bukkitConfig.getString("data.logfile")));

        setInactiveDays(bukkitConfig.getInt("players.inactiveDays", getInactiveDays()));
        setMinPlaytime(bukkitConfig.getInt("players.minPlaytime", getMinPlaytime()));
        setUpdateInactive(bukkitConfig.getBoolean("players.updateInactive", isUpdateInactive()));
        setProfileUpdateInterval(bukkitConfig.getInt("players.profileUpdateInterval", getProfileUpdateInterval()));

        setExcludeBanned(bukkitConfig.getBoolean("players.excludeBanned", isExcludeBanned()));
        setExcludeOps(bukkitConfig.getBoolean("players.excludeOps", isExcludeOps()));
        
        getExcludeUUIDs().addAll(bukkitConfig.getStringList("players.excludeUUIDs"));

        setBronzeMedalWeight(bukkitConfig.getInt("crown.bronze", getBronzeMedalWeight()));
        setSilverMedalWeight(bukkitConfig.getInt("crown.silver", getSilverMedalWeight()));
        setGoldMedalWeight(bukkitConfig.getInt("crown.gold", getGoldMedalWeight()));

        setDefaultLanguage(bukkitConfig.getString("client.defaultLanguage", getDefaultLanguage()));
        setPlayersPerPage(bukkitConfig.getInt("client.playersPerPage", getPlayersPerPage()));
        setPlayerCacheUUIDPrefix(bukkitConfig.getInt("client.playerCacheUUIDPrefix", getPlayerCacheUUIDPrefix()));
        setServerName(bukkitConfig.getString("client.serverName", getServerName()));
        setShowLastOnline(bukkitConfig.getBoolean("client.showLastOnline", isShowLastOnline()));
    }

    public String getWebSubdir() {
        return webSubdir;
    }

    public void setWebSubdir(String subdirName) {
        this.webSubdir = subdirName;
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

    public boolean isSkinsRestorerEnabled() {
        return skinsRestorerEnabled;
    }

    public void setSkinsRestorerEnabled(boolean skinsRestorerEnabled) {
        this.skinsRestorerEnabled = skinsRestorerEnabled;
    }
}
