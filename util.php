<?
    /**
     * Utilities
     */

    function findStat($id) {
        global $stats;
    
        if(array_key_exists($id, $stats)) {
            return $stats[$id];
        } else {
            return FALSE;
        }
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
    
    function createPlayerWidget($uuid) {
        if($uuid !== FALSE) {
            return
                '<span class="player">' .
                '<img src="' . getPlayerSkin($uuid) . '"/><span><canvas/></span>' .
                getPlayerName($uuid) .
                '</span>';
        } else {
            return '<div class="player-nobody"><div>Nobody</div></div>';
        }
    }
?>