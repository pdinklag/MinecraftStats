<?
    /**
     * Updates or creates the prepared stats from the raw stats.
     */
     
    require_once('config.php');
    require_once('util.php');
    
    error_reporting(E_ALL ^ E_NOTICE);
    
    //Resolves a UUID to the ingame name by contacting Mojang's servers
    function lookupPlayerName($uuid) {
        $uuid = str_replace("-", "", $uuid);
        $json = json_decode(file_get_contents("https://sessionserver.mojang.com/session/minecraft/profile/$uuid"), true);
        return $json['name'];
    }
    
    //Comparator for rankings (using usort)
    function compareRankingEntries($a, $b) {
        global $players;
    
        if(is_array($a['score'])) {
            $d = $b['score']['score'] - $a['score']['score'];
        } else {
            $d = $b['score'] - $a['score'];
        }
        
        if($d == 0) {
            return strcasecmp($players[$a['id']]['name'], $players[$b['id']]['name']);
        } else {
            return $d;
        }
    }
    
    //Read command-line options
    $opts = getopt('', ['update-playercache']);
    $forcePlayerCacheUpdate = isset($opts['update-playercache']);
    
    //Scan raw data dir
    $playerStats = [];
    if(is_dir($rawDataDir)) {
        //Read usercache
        $userCache = [];
        $userCacheFile = 'usercache.json';
        if(is_file("$rawDataDir/$userCacheFile")) {
            echo("Reading user cache ...\n");
            $userCacheJSON = json_decode(file_get_contents("$rawDataDir/$userCacheFile"), true);
            foreach($userCacheJSON as $entry) {
                $userCache[$entry['uuid']] = $entry['name'];
            }
        }
    
        //Scan for player JSON files
        echo("Scanning raw data ...\n");
        $dir = opendir($rawDataDir);
        while($f = readdir($dir)) {
            if($f == $userCacheFile) {
                continue;
            }
        
            $jsonFile = "$rawDataDir/$f";
            if(is_file($jsonFile)) {
                //Extract UUID from file name
                $uuid = substr($f, 0, -5); //5 = length of ".json"
                
                //Check if UUID is in player cache
                if($forcePlayerCacheUpdate || !array_key_exists($uuid, $players)) {
                    //if not, look it up
                    echo("Looking up new UUID $uuid ... ");
                    
                    if(isset($userCache[$uuid])) {
                        //it's in the local user cache!
                        $playerName = $userCache[$uuid];
                    } else {
                        //fetch from Mojang
                        $playerName = lookupPlayerName($uuid);
                    }
                    
                    $players[$uuid] = ['name' => $playerName];
                    echo($players[$uuid]['name'] . "\n");
                } else {
                    //if yes, update the name from the user cache - it may have changed
                    if(isset($userCache[$uuid])) {
                        $players[$uuid]['name'] = $userCache[$uuid];
                    }
                }
                
                $lastOnline = filemtime($jsonFile);
                $players[$uuid]['date'] = $lastOnline;
                
                //Parse JSON
                $json = json_decode(file_get_contents($jsonFile), true);
                
                //Count stats
                foreach($stats as $id => $stat) {
                    $value = getStatProgressForPlayer($id, $json);
                    if($value !== FALSE) {
                        if(!isInactive($lastOnline) || isPlayerListStat($id)) {
                            //Insert into ranking
                            $stats[$id]['ranking'][] = ['id' => $uuid, 'score' => $value];
                        }
                        
                        //Set player stat
                        $playerStats[$uuid][$id] = ['score' => $value];
                    }
                }
            }
        }
        closedir($dir);
    }
    
    //Create data directories if necessary
    if(!is_dir($dataDir)) {
        mkdir($dataDir, 0755);
    }
    
    if(!is_dir($statDataDir)) {
        mkdir($statDataDir, 0755);
    }
    
    if(!is_dir($playerDataDir)) {
        mkdir($playerDataDir, 0755);
    }
    
    //Save players
    echo("Saving player cache ...\n");
    file_put_contents($playerCacheFile, serialize($players));
    
    //Sort and save stat rankings, compute awards and hall of fame
    $awards = [];
    $hof = [];
    
    foreach($stats as $id => $stat) {
        echo("Saving data for $id ...\n");
        
        if(isset($stat['ranking'])) {
            //Sort ranking
            usort($stat['ranking'], 'compareRankingEntries');
            
            //Save stat ranking for players
            foreach($stat['ranking'] as $rank => $entry) {
                $uuid = $entry['id'];
            
                if(!array_key_exists($uuid, $playerStats)) {
                    $playerStats[$uuid] = [];
                }
                
                if($rank < 3) {
                    $e = safeGet($uuid, $hof, []);
                    $e['id'] = $uuid; //save for sorter
                    switch($rank) {
                        case 0:
                            safeInc('gold', $e, 1);
                            safeInc('score', $e, $goldMedalScore);
                            break;
                        
                        case 1:
                            safeInc('silver', $e, 1);
                            safeInc('score', $e, $silverMedalScore);
                            break;
                        
                        case 2:
                            safeInc('bronze', $e, 1);
                            safeInc('score', $e, $bronzeMedalScore);
                            break;
                    }
                    $hof[$uuid] = $e;
                }
                
                $playerStats[$uuid][$id]['rank'] = $rank;
            }
            
            //Create award entry
            $awards[$id] = $stat['ranking'][0];
            
            //Save stat data
            file_put_contents("$statDataDir/" . $id, serialize($stat['ranking']));
        }
    }
    
    //Save player stats
    foreach($playerStats as $id => $pstat) {
        echo("Saving data for $id ...\n");
        file_put_contents("$playerDataDir/" . $id, serialize($pstat));
    }
    
    //Save awards
    echo("Saving awards ...\n");
    file_put_contents($awardsFile, serialize($awards));
    
    //Create award output
    if($awardOutputFile) {
        echo("Generating award output ...\n");
        $f = fopen($awardOutputFile, 'w');
        foreach($stats as $id => $stat) {
            if(array_key_exists($id, $awards)) {
                $award = $awards[$id];
                
                fwrite($f,
                    str_replace('%A%', $stat['award'],
                    str_replace('%D%', $stat['desc'],
                    str_replace('%W%', getPlayerName($award['id']),
                    str_replace('%S%', getStatDisplayValue($stat, $award['score']), $awardOutputFormat)))));
            }
        }
        
        fclose($f);
    }
    
    //Sort and save Hall of Fame
    echo("Saving hall of fame\n");
    uasort($hof, 'compareRankingEntries');
    file_put_contents($hofFile, serialize($hof));
    
    //Save last update
    echo("Saving last update time ...\n");
    file_put_contents($lastUpdateFile, serialize(time()));
?>
