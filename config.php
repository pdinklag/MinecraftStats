<?
    /**
     * General configuration.
     */
    require_once("util.php");

    //Data structure
    $dataDir = "data";
    $rawDataDir = "raw";
    
    $playerCacheFile = "$dataDir/players.txt";
    
    $hofFile = "$dataDir/hof.txt";
    $lastUpdateFile = "$dataDir/lastUpdate";
    
    $statDataDir = "$dataDir/stats";
    $playerDataDir = "$dataDir/players";
    
    //General Settings
    $title = "DVGaming.COM Snapshot";
    $disclaimer = "";
    
    //Icons
    $awardIconDir = "icons";
    $defaultIcon = "minecraft-wiki/64px-No_image.svg.png";
    
    //Skins
    $defaultSkin = "skins/steve.png";

    //Load Stats configuration
    require("config-stats.php");

    //Load player data
    if(is_file($playerCacheFile)) {
        $players = unserialize(file_get_contents($playerCacheFile));
    } else {
        $players = [];
    }
?>
