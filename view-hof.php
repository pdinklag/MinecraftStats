<?
    /**
     * Viewing the hall of fame.
     *
     * Included by index.php when $_GET['hof'] is set.
     */
    
    //Load HOF
    if(is_file($hofFile)) {
        $hof = unserialize(file_get_contents($hofFile));
    } else {
        $hof = [];
    }
?>
<div id="nav"><a href="index.php">Awards</a></div>
<div id="header">
    Hall of Fame
</div>
<div id="listing-wrapper">
    <div class="listing">
        <div id="king">
            <p>The King of <? echo($title); ?> is:</p>
            <? echo(createPlayerWidget(current($hof)['id'], 28, '<img class="crown" src="img/fatcow/crown_gold.png"/>')); ?>
        </div>
        <p>
            Crown score ranking:<br/>
            The crown score is calculated using the medals a player holds.<br/>
            A gold medal is worth <? echo($goldMedalScore); ?> points, a silver medal <? echo($silverMedalScore); ?> points
            and a bronze medal <? echo($bronzeMedalScore . ($bronzeMedalScore > 1 ? ' points' : ' point')); ?>.
        </p>
        <table class="listing">
            <colgroup>
                <col style="width: 10%"/>
                <col style="width: 45%"/>
                <col style="width: 10%"/>
                <col style="width: 10%"/>
                <col style="width: 10%"/>
                <col style="width: 15%"/>
            </colgroup>
            <tbody>
                <tr>
                    <th>Rank</th>
                    <th>Player</th>
                    <th><img src="img/fatcow/medal_award_bronze.png"/></th>
                    <th><img src="img/fatcow/medal_award_silver.png"/></th>
                    <th><img src="img/fatcow/medal_award_gold.png"/></th>
                    <th>Crown Score</th>
                </tr>
                <?
                    $i = 0;
                    foreach($hof as $id => $e) {
                        ?>
                        <tr>
                            <td class="rank <? echo("place$i crown$i"); ?>"><? echo($i + 1); ?></td>
                            <td class="player <? echo("place$i"); ?>"><? echo(createPlayerWidget($e['id'], 24)); ?></td>
                            <td class="center score-bronze <? echo("place$i"); ?>"><? echo(safeGet('bronze', $e, 0)); ?></td>
                            <td class="center score-silver <? echo("place$i"); ?>"><? echo(safeGet('silver', $e, 0)); ?></td>
                            <td class="center score-gold <? echo("place$i"); ?>"><? echo(safeGet('gold', $e, 0)); ?></td>
                            <td class="center score <? echo("place$i"); ?>"><? echo(safeGet('score', $e, 0)); ?></td>
                        </tr>
                        <?
                        $i++;
                    }
                ?>
            </tbody>
        </table>
    </div>
</div>
