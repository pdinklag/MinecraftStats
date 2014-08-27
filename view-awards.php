<?
    /**
     * Viewing the awards page.
     *
     * Included by index.php no specific site is to be viewed.
     */
    if(is_file($awardsFile)) {
        $awards = unserialize(file_get_contents($awardsFile));
    } else {
        $awards = [];
    }
?>
<div id="nav"><a href="?stat=stat.playOneMinute">List of players</a></div>
<div id="header">Awards</div>
<div id="awards">
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
                        if(array_key_exists($id, $awards)) {
                            $awardWinner = createPlayerWidget($awards[$id]['id'], 24);
                            $awardText = $stat['desc'] . ': <span class="award-score">' . getStatDisplayValue($stat, $awards[$id]['score']) . '</span>';
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