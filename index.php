<?
    require_once('config.php');
    
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
        return
            '<span class="player">' .
            '<img src="' . getPlayerSkin($uuid) . '"/><span><canvas/></span>' .
            getPlayerName($uuid) .
            '</span>';
    }
    
    //Check if a certain stat is to be viewed
    if(isset($_GET["stat"])) {
        $id = $_GET["stat"];
        if(isset($stats[$id])) {
            $viewStat = $stats[$id];
        
            //Load ranking
            $rankingFile = "$dataDir/" . $id;
            if(is_file($rankingFile)) {
                $viewStat['ranking'] = unserialize(file_get_contents($rankingFile));
            } else {
                $viewStat['ranking'] = [];
            }
        } else {
            die("Unknown stat.");
        }
    }
?>
<!DOCTYPE html>
<html>
<head>
    <title><? echo($title); ?></title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<div id="last-update">
    The statistics were last updated 
    <?
        if(is_file($lastUpdateFile)) {
            $lastUpdate = unserialize(file_get_contents($lastUpdateFile));
            
            $delta = (time() - $lastUpdate);
            $deltaMinutes = (int)($delta / 60);
            
            if($delta >= 120) {
                echo("$deltaMinutes minutes ago.");
            } else if($delta >= 60) {
                echo("a minute ago.");
            } else {
                echo("$delta seconds ago.");
            }
        }
    ?>
</div>
<h1><? echo($title); ?></h1>
<?
    if(isset($viewStat)) {
        ?>
        <div id="back-to-index">&larr; <a href="index.php">Back to Hall of Fame</a></div>
        <div id="ranking-header">
            <span class="icon"><img src="<? echo(getStatIcon($viewStat)); ?>"/></span>
            <? echo($viewStat['award']); ?>
        </div>
        <div id="ranking-wrapper">
            <div id="ranking">
                <p>Ranking for the "<? echo($viewStat['award'])?>" award (<? echo($viewStat['desc'])?>):</p>
                <table>
                    <tr>
                        <th>Rank</th>
                        <th>Player</th>
                        <th><? echo($viewStat['desc'])?></th>
                    </tr>
                    <?
                        foreach($viewStat['ranking'] as $i => $e) {
                            ?>
                            <tr>
                                <td class="rank <? echo("place$i medal$i"); ?>"><? echo($i + 1); ?></td>
                                <td class="player <? echo("place$i"); ?>"><? echo(createPlayerWidget($e[0])); ?></td>
                                <td class="score <? echo("place$i"); ?>"><? echo(getStatDisplayValue($viewStat, $e[1])); ?></td>
                            </tr>
                            <?
                        }
                    ?>
                </table>
            </div>
        </div>
        <?
    } else {
        //Hall of Fame
        if(is_file($hofFile)) {
            $hof = unserialize(file_get_contents($hofFile));
        } else {
            $hof = [];
        }
        
        ?>
        <div id="hof-header">Hall of Fame</div>
        <div id="hof">
            <?
                //Stat sorter
                function compareStats($a, $b) {
                    return strcasecmp($a['award'], $b['award']);
                }
                
                uasort($stats, 'compareStats');
                foreach($stats as $id => $stat) {
                    ?>
                        <div class="award-box">
                            <div class="award-icon">
                                <img src="<? echo(getStatIcon($stat)); ?>"/>
                            </div>
                            <div class="award-title">
                                <a href="?stat=<? echo($id); ?>"><? echo($stat['award']); ?></a>
                            </div>
                            
                            <?
                                if(array_key_exists($id, $hof)) {
                                    $awardWinner = createPlayerWidget($hof[$id][0]);
                                    $awardText = $stat['desc'] . ': <span class="award-score">' . getStatDisplayValue($stat, $hof[$id][1]) . '</span>';
                                } else {
                                    $awardWinner = '<span class="award-winner-nobody">Nobody yet</span>';
                                    $awardText = '(' . $stat['desc'] . ')';
                                }
                            ?>
                            
                            <div class="award-winner-box">
                                <div class="award-winner">
                                    <? echo($awardWinner); ?>
                                </div>
                                <div class="award-text">
                                    <? echo($awardText); ?></span>
                                </div>
                            </div>
                        </div>
                    <?
                }
            ?>
        </div>
<?
    }
?>
<div id="foot-wrapper">
    &nbsp;
    <div id="foot">
        Written by Patrick Dinklage a.k.a. "pdinklag".
        <? if(isset($disclaimer)) { ?>
            <div id="disclaimer"><? echo($disclaimer); ?></div>
        <? } ?>
    </div>
</div>

<script type="text/javascript" src="jquery-2.1.1.min.js"></script>
<script type="text/javascript">
    $(".player img").load(function(event) {
        var img = event.target;
        var canvas = img.parentNode.getElementsByTagName("canvas")[0];
        
        var ctx = canvas.getContext('2d');
        ctx.imageSmoothingEnabled = false;
        ctx.drawImage(img, 8, 8, 8, 8, 0, 0, canvas.width, canvas.height);
    }).each(function() {
        if(this.complete) {
            $(this).load();
        }
    });
</script>

</body>
</html>
