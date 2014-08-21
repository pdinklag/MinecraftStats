<?
    /**
     * General configuration.
     */

    //Data structure
    $dataDir = "data";
    $rawDataDir = "raw";
    
    $playerCacheFile = "$dataDir/players.txt";
    $hofFile = "$dataDir/hof.txt";
    $lastUpdateFile = "$dataDir/lastUpdate";
    
    //General Settings
    $serverName = "DVGaming.COM Snapshot";
    $title = $serverName;
    
    //Icons
    $awardIconDir = "icons";
    $defaultIcon = "minecraft-wiki/64px-No_image.svg.png";

    //Load Stats configuration
    require("config-stats.php");

    //Load player data
    if(is_file($playerCacheFile)) {
        $players = unserialize(file_get_contents($playerCacheFile));
    } else {
        $players = [];
    }
?>
