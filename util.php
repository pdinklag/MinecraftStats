<?
    /**
     * Utilities
     */
    date_default_timezone_set('Europe/Berlin');
     
    function findStat($id) {
        global $stats;
    
        if(array_key_exists($id, $stats)) {
            return $stats[$id];
        } else {
            return FALSE;
        }
    }
    
    function formatDate($t) {
        return date('M d, Y - H:i', $t);
    }
    
    function compareStatAwardNames($a, $b) {
        return strcasecmp($a['award'], $b['award']);
    }
    
    function sortStatsByAwardName() {
        global $stats;
        uasort($stats, 'compareStatAwardNames');
    }
    
    function getStatIcon($stat) {
        global $awardIconDir, $defaultIcon;
    
        if(isset($stat['icon'])) {
            return "$awardIconDir/" . $stat['icon'];
        } else {
            return "$awardIconDir/$defaultIcon";
        }
    }
    
    function getStatDisplayValue($stat, $value) {
        if(isset($stat['displayFunc'])) {
            return call_user_func($stat['displayFunc'], $value);
        } else {
            return $value;
        }
    }
    
    function getPlayerName($uuid) {
        global $players;
        
        if(array_key_exists($uuid, $players)) {
            return $players[$uuid]['name'];
        } else {
            return $uuid;
        }
    }
    
    function getPlayerSkin($uuid) {
        global $players, $defaultSkin;
        
        if(array_key_exists($uuid, $players)) {
            $info = $players[$uuid];
            if(isset($info['skinUrl'])) {
                return $info['skinUrl'];
            } else {
                return $defaultSkin;
            }
        } else {
            return $defaultSkin;
        }
    }
    
    function getStatProgressForPlayer($statId, $json) {
        global $stats;
        
        $stat = findStat($statId);
        if($stat) {
            if(isset($stat['provider'])) {
                $value = call_user_func($stat['provider'], $json);
                return $value;
            } else if(array_key_exists($statId, $json)) {
                return $json[$statId];
            }
        }
        
        return FALSE;
    }
    
    function createPlayerWidget($uuid, $size, $inject = '') {
        if($uuid !== FALSE) {
            return
                '<span class="player">' .
                '<img src="' . getPlayerSkin($uuid) . '"/><span><canvas width="' . $size . '" height="'.$size.'"/></span>' .
                "<a href='?player=$uuid'>" . getPlayerName($uuid) . '</a>' .
                $inject .
                '</span>';
        } else {
            return '<div class="player-nobody"><div>Nobody</div></div>';
        }
    }
    
    function safeGet($key, $arr, $def) {
        if(array_key_exists($key, $arr)) {
            return $arr[$key];
        } else {
            return $def;
        }
    }
    
    function safeInc($key, &$arr, $inc) {
        if(array_key_exists($key, $arr)) {
            $arr[$key] += $inc;
        } else {
            $arr[$key] = $inc;
        }
    }
?>