<?
    /**
     * Viewing a specific player.
     *
     * Included by index.php when $_GET['player'] is set.
     */
    $playerId = $_GET["player"];
    if(isset($players[$playerId])) {
        $player = $players[$playerId];

        //Load player JSON
        $jsonFile = "$rawDataDir/$playerId.json";
        if(is_file($jsonFile)) {
            $playerJson = json_decode(file_get_contents($jsonFile), true);
        } else {
            $playerJson = [];
        }
    } else {
        die("Unknown player.");
    }
?>
<div id="back-to-index">&larr; <a href="index.php">Back to Hall of Fame</a></div>
<div id="ranking-header">
    <? echo(createPlayerWidget($playerId, 64)); ?>
</div>
<div id="ranking-wrapper">
    <div id="ranking">
        <p>Statistics for <? echo(getPlayerName($playerId)); ?> by awards:</p>
        <table>
            <colgroup>
                <col style="width:40%;"/>
                <col style="width:20%;"/>
                <col style="width:25%;"/>
                <col style="width:15%;"/>
            </colgroup>
            <tr>
                <th>Stat</th>
                <th>Score</th>
                <th>Award</th>
                <th>Rank</th>
            </tr>
            <?
                sortStatsByAwardName();
                foreach($stats as $id => $stat) {
                    $value = getStatProgressForPlayer($id, $playerJson);
                    if($value !== FALSE) {
                        $value = getStatDisplayValue($stat, $value);
                    } else {
                        $value = "&mdash;";
                    }
                    
                    ?>
                    <tr>
                        <td class="stat"><? echo($stat['desc']); ?>:</td>
                        <td class="score"><? echo($value); ?></td>
                        <td class="award"><span class="icon"><img src="<? echo(getStatIcon($stat)); ?>"/></span> <a href="?stat=<? echo($id); ?>"><? echo($stat['award']); ?></a></td>
                        <td class="rank"><i>(TODO)</i></td>
                    </tr>
                    <?
                }
            ?>
        </table>
    </div>
</div>
