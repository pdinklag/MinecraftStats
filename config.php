<?
    /**
     * General configuration.
     */
    require_once("util.php");
    
    $mcstatsVersion = "1.00";
    
    //Time zone
    date_default_timezone_set('Europe/Berlin');
    $timezone = 'CEST';

    //Data structure
    $dataDir = "data";
    $rawDataDir = "raw";
    
    $playerCacheFile = "$dataDir/players.txt";
    
    $hofFile = "$dataDir/hof.txt";
    $awardsFile = "$dataDir/awards.txt";
    $lastUpdateFile = "$dataDir/lastUpdate";
    
    $statDataDir = "$dataDir/stats";
    $playerDataDir = "$dataDir/players";
    
    //Award output - %A% = award name, %W% = Winner, %D% = Award description, %S% = Score
    $awardOutputFile = "$dataDir/awardsOutput.txt";
    $awardOutputFormat = "%A%;%W%;%D%;%S%\n";
    
    //General Settings
    $title = "DVG Snapshot Stats";
    $inactiveTime = 604800; //seven days
    
    //Paging
    $itemsPerPage = 50;
    
    //Hall of Fame score settings
    $goldMedalScore   = 4;
    $silverMedalScore = 2;
    $bronzeMedalScore = 1;
    
    //Icons
    $awardIconDir = "img/icons";
    $defaultIcon = "minecraft-wiki/64px-No_image.svg.png";
    
    //Skins
    $defaultSkins = ["img/skins/steve.png", "img/skins/alex.png"];

    //Load Stats configuration
    require("config-stats.php");

    //Load player data
    if(is_file($playerCacheFile)) {
        $players = unserialize(file_get_contents($playerCacheFile));
    } else {
        $players = [];
    }
?>
