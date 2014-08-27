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
        
        $showLastOnline = ($viewStatId == 'stat.playOneMinute');
    } else {
        die("Unknown stat.");
    }
?>
<div id="nav"><a href="index.php">Awards</a></div>
<div id="header">
    <span class="icon"><img src="<? echo(getStatIcon($viewStat)); ?>"/></span>
    <? echo($viewStat['award']); ?>
</div>
<div id="listing-wrapper">
    <div class="listing">
        <p>Ranking for the "<? echo($viewStat['award'])?>" award (<? echo($viewStat['desc'])?>):</p>
        <table class="listing">
            <tbody>
            <tr>
                <th>Rank</th>
                <th>Player</th>
                <th><? echo($viewStat['desc'])?></th>
                <?
                    if($showLastOnline) {
                        ?>
                        <th>Last Online</th>
                        <?
                    }
                ?>
            </tr>
            <?
                foreach($viewStat['ranking'] as $i => $e) {
                    ?>
                    <tr>
                        <td class="rank <? echo("place$i medal$i"); ?>"><? echo($i + 1); ?></td>
                        <td class="player <? echo("place$i"); ?>"><? echo(createPlayerWidget($e['id'], 24)); ?></td>
                        <td class="score <? echo("place$i"); ?>"><? echo(getStatDisplayValue($viewStat, $e['score'])); ?></td>
                        <?
                            if($showLastOnline) {
                                ?>
                                <td class="date <? echo("place$i"); ?>"><? echo(formatDate($players[$e['id']]['date'])); ?></td>
                                <?
                            }
                        ?>
                    </tr>
                    <?
                }
            ?>
            </tbody>
        </table>
    </div>
</div>
