<?
    /**
     * Updates or creates the prepared stats from the raw stats.
     */
     
    require_once('config.php');
    
    error_reporting(E_ALL ^ E_NOTICE);
    
    //Resolves a UUID to the last ingame name used
    function lookupPlayerInfo($uuid) {
        $uuid = str_replace("-", "", $uuid);
        $json = json_decode(file_get_contents("https://sessionserver.mojang.com/session/minecraft/profile/$uuid"), true);
        
        $info = [];
        $info['name'] = $json['name'];
        
        //find skin
        foreach($json['properties'] as $prop) {
            if($prop['name'] == 'textures') {
                //decode the value set...
                $jsonTextures = json_decode(base64_decode($prop['value']), true);
                $info['skinUrl'] = $jsonTextures['textures']['SKIN']['url'];
                break;
            }
        }
        
        return $info;
    }
    
    //Comparator for rankings (using usort)
    function compareRankingEntries($a, $b) {
        global $players;
    
        $d = $b[1] - $a[1];    
        if($d == 0) {
            return strcasecmp($players[$a[0]]['name'], $players[$b[0]]['name']);
        } else {
            return $d;
        }
    }
    
    //Scan raw data dir
    echo("Scanning raw data ...\n");
    
    if(is_dir($rawDataDir)) {
        $dir = opendir($rawDataDir);
        while($f = readdir($dir)) {
            $jsonFile = "$rawDataDir/$f";
            if(is_file($jsonFile)) {
                //Extract UUID from file name
                $uuid = substr($f, 0, -5); //5 = length of ".json"
                
                //Check if UUID is in player cache
                if(!array_key_exists($uuid, $players)) {
                    //if not, look it up
                    echo("Looking up new UUID $uuid ... ");
                    $info = lookupPlayerInfo($uuid);
                    $players[$uuid] = $info;
                    
                    //DEBUG
                    echo($info['name'] . ", skin: " . $info['skinUrl'] . "\n");
                } else {
                    $info = $players[$uuid];
                }
                
                //Parse JSON
                $json = json_decode(file_get_contents($jsonFile), true);
                
                //Count stats
                foreach($stats as $i => $stat) {
                    if(isset($stat['provider'])) {
                        $value = call_user_func($stat['provider'], $json);
                        if($value !== FALSE) {
                            $stats[$i]['ranking'][] = [$uuid, $value];
                        }
                    } else if(array_key_exists($stat['id'], $json)) {
                        $stats[$i]['ranking'][] = [$uuid, $json[$stat['id']]];
                    }
                }
            }
        }
        closedir($dir);
    }
    
    //Create data dir if necessary
    if(!is_dir($dataDir)) {
        mkdir($dataDir, 0755);
    }
    
    //Save players
    echo("Saving player cache ...\n");
    file_put_contents($playerCacheFile, serialize($players));
    
    //Sort and save stat rankings, compute HOF
    $hof = [];
    foreach($stats as $stat) {
        echo("Saving data for " . $stat['id'] . " ...\n");
        
        if(isset($stat['ranking'])) {
            usort($stat['ranking'], "compareRankingEntries");
            $hof[$stat['id']] = $stat['ranking'][0];
            
            file_put_contents("$dataDir/" . $stat['id'], serialize($stat['ranking']));
        }
    }
    
    //Save HOF
    echo("Saving HOF ...\n");
    file_put_contents($hofFile, serialize($hof));
    
    //Save last update
    echo("Saving last update time ...\n");
    file_put_contents($lastUpdateFile, serialize(time()));
    
    //Debug output
    /*
    echo("<hr/>");
    var_dump($players);
    echo("<hr/>");
    var_dump($stats);
    echo("<hr/>");
    var_dump($hof);
    */
?>
