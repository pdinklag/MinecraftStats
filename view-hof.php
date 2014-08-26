<?
    /**
     * Viewing the hall of fame.
     *
     * Included by index.php no specific site is to be viewed.
     */
    if(is_file($hofFile)) {
        $hof = unserialize(file_get_contents($hofFile));
    } else {
        $hof = [];
    }
?>
<div id="hof-header">Hall of Fame</div>
<div id="hof">
    <?
        sortStatsByAwardName();
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
                            $awardWinner = createPlayerWidget($hof[$id]['id'], 24);
                            $awardText = $stat['desc'] . ': <span class="award-score">' . getStatDisplayValue($stat, $hof[$id]['score']) . '</span>';
                        } else {
                            $awardWinner = createPlayerWidget(FALSE, 24);
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