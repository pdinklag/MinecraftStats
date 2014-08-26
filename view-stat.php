<?
    /**
     * Viewing a specific stat.
     *
     * Included by index.php when $_GET['stat'] is set.
     */
    $viewStatId = $_GET["stat"];
    if(isset($stats[$viewStatId])) {
        $viewStat = $stats[$viewStatId];

        //Load ranking
        $rankingFile = "$statDataDir/" . $viewStatId;
        if(is_file($rankingFile)) {
            $viewStat['ranking'] = unserialize(file_get_contents($rankingFile));
        } else {
            $viewStat['ranking'] = [];
        }
    } else {
        die("Unknown stat.");
    }
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
                        <td class="player <? echo("place$i"); ?>"><? echo(createPlayerWidget($e['id'], 24)); ?></td>
                        <td class="score <? echo("place$i"); ?>"><? echo(getStatDisplayValue($viewStat, $e['score'])); ?></td>
                    </tr>
                    <?
                }
            ?>
        </table>
    </div>
</div>
