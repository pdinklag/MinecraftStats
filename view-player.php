<?
    /**
     * Viewing a specific player.
     *
     * Included by index.php when $_GET['player'] is set.
     */
    $playerId = $_GET["player"];
    if(isset($players[$playerId])) {
        $player = $players[$playerId];

        //Load player stats
        $dataFile = "$playerDataDir/$playerId";
        if(is_file($dataFile)) {
            $pstats = unserialize(file_get_contents($dataFile));
        } else {
            $pstats = [];
        }

    } else {
        die("Unknown player.");
    }
?>
<div id="nav">&larr; <a href="index.php">Back to Hall of Fame</a></div>
<div id="header">
    <? echo(createPlayerWidget($playerId, 64)); ?>
</div>
<div id="listing-wrapper">
    <div class="listing">
        <p class="date">Last online: <? echo(date('D, M d, Y - H:i', $players[$playerId]['date']) . ' (CEST)'); ?></p>
        <p>Medals held by <? echo(getPlayerName($playerId)); ?>:</p>
        <?
            //Count medals
            $gold = 0;
            $silver = 0;
            $bronze = 0;
        
            foreach($pstats as $id => $data) {
                switch($data['rank']) {
                    case 0:
                        $gold++;
                        break;

                    case 1:
                        $silver++;
                        break;
                    
                    case 2:
                        $bronze++;
                        break;
                }
            }
        ?>
        <table class="medals">
            <colgroup>
                <col style="width:50%;"/>
                <col style="width:50%;"/>
            </colgroup>
            <tbody>
                <tr>
                    <td class="medal"><img src="img/fatcow/medal_award_gold.png"/></td>
                    <td class="count"><? echo($gold); ?></td>
                </tr>
                <tr>
                    <td class="medal"><img src="img/fatcow/medal_award_silver.png"/></td>
                    <td class="count"><? echo($silver); ?></td>
                </tr>
                <tr>
                    <td class="medal"><img src="img/fatcow/medal_award_bronze.png"/></td>
                    <td class="count"><? echo($bronze); ?></td>
                </tr>
            </tbody>
        </table>
    </div>
    <hr/>
    <div class="listing">
        <p>Statistics by award (<a href="?raw=<? echo($playerId); ?>">view raw data</a>):</p> 
        <table class="listing">
            <colgroup>
                <col style="width:40%;"/>
                <col style="width:15%;"/>
                <col style="width:35%;"/>
                <col style="width:10%;"/>
            </colgroup>
            <tbody>
                <tr>
                    <th>Stat</th>
                    <th>Score</th>
                    <th>Award</th>
                    <th>Rank</th>
                </tr>
                <?
                    sortStatsByAwardName();
                    foreach($stats as $id => $stat) {
                        if(array_key_exists($id, $pstats)) {
                            $score = getStatDisplayValue($stat, $pstats[$id]['score']);
                            $rank = $pstats[$id]['rank'];
                        } else {
                            unset($score);
                            unset($rank);
                        }

                        ?>
                        <tr>
                            <td class="stat">
                                <? echo($stat['desc']); ?>:
                            </td>
                            <td class="score">
                                <?
                                    echo(isset($score) ? $score : '&mdash;');
                                ?>
                            </td>
                            <td class="award <? if(isset($rank)) { echo("place$rank"); } ?>"><span class="icon">
                                <img src="<? echo(getStatIcon($stat)); ?>"/></span> <a href="?stat=<? echo($id); ?>"><? echo($stat['award']); ?></a>
                            </td>
                            <td class="rank <? if(isset($rank)) { echo("place$rank medal$rank"); } ?>">
                                <?
                                    if(isset($rank)) {
                                        echo('#' . ($rank + 1));
                                    } else {
                                        echo('&mdash;');
                                    }
                                ?>
                            </td>
                        </tr>
                        <?
                    }
                ?>
            </tbody>
        </table>
    </div>
</div>
