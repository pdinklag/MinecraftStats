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
        
        $isPlayerList = isPlayerListStat($viewStatId);
        
        //Paging
        $ranking = $viewStat['ranking'];
        
        $numItems = count($ranking);
        $numPages = (int)(count($ranking) / $itemsPerPage) + 1;
        
        if(isset($_GET['all'])) {
            $page = 'all';
            $start = 0;
            $num = $numItems;
        } else {
            $page = 1;
            if(isset($_GET['page'])) {
                $page = (int)$_GET['page'];
            }
            
            $start = ($page - 1) * $itemsPerPage;
            $num   = $itemsPerPage;
        }
    } else {
        die("Unknown stat.");
    }
?>
<div id="header">
    <span class="icon"><img src="<? echo(getStatIcon($viewStat)); ?>"/></span>
    <? echo($viewStat['award']); ?>
</div>
<div id="listing-wrapper">
    <div class="listing">
        <p>Ranking for the "<? echo($viewStat['award'])?>" award (<? echo($viewStat['desc'])?>):</p>
        <table class="page">
            <colgroup>
                <col style="width: 33%"/>
                <col style="width: 34%"/>
                <col style="width: 33%"/>
            </colgroup>
            <tbody><tr>
            <td class="left">
                <?
                    if($page == 'all' || $page > 1) {
                ?>
                    <a href="?stat=<? echo($viewStatId); ?>">&lt;&lt; First</a>
                    
                    <? if($page != 'all') {?>
                    | <a href="?stat=<? echo($viewStatId); ?>&page=<? echo($page - 1); ?>">&lt; Previous</a>
                    <?}?>
                <?
                    }
                ?>
            </td>
            <td class="center">
                Showing
                <?
                if($page == 'all') {
                    ?>
                    all <? echo($numPages); ?> pages.
                    <?
                } else {
                    ?>
                    page <? echo($page); ?> of <? echo($numPages); ?>. (<a href="?stat=<? echo($viewStatId); ?>&all">show all</a>)
                    <?
                }
                ?>
            </td>
            <td class="right">
                <?
                    if($page == 'all' || $page < $numPages) {
                ?>
                    <? if($page != 'all') {?>
                    <a href="?stat=<? echo($viewStatId); ?>&page=<? echo($page + 1); ?>">Next &gt;</a> |
                    <?}?>
                    
                    <a href="?stat=<? echo($viewStatId); ?>&page=<? echo($numPages); ?>">Last &gt;&gt;</a>
                <?
                    }
                ?>
            </td>
            </tr></tbody>
        </table>
        <table class="listing">
            <tbody>
            <tr>
                <th>Rank</th>
                <th>Player</th>
                <th><? echo($viewStat['desc'])?></th>
                <?
                    if($isPlayerList) {
                        ?>
                        <th>Last Online</th>
                        <?
                    }
                ?>
            </tr>
            <?
                for($k = 0; $k < $num && ($start + $k) < $numItems; $k++) {
                    $i = $start + $k;
                    $e = $ranking[$i];
                    ?>
                    <tr>
                        <td class="rank <? echo("place$i medal$i"); ?>"><? echo($i + 1); ?></td>
                        <td class="player <? echo("place$i"); ?>"><? echo(createPlayerWidget($e['id'], 24)); ?></td>
                        <td class="score <? echo("place$i"); ?>"><? echo(getStatDisplayValue($viewStat, $e['score'])); ?></td>
                        <?
                            if($isPlayerList) {
                                $lastOnline = getPlayerLastOnline($e['id']);
                                
                                ?>
                                <td class="date <? if(isPlayerInactive($e['id'])) { echo('inactive'); } ?> <? echo("place$i"); ?>"><? echo(formatDate($lastOnline)); ?></td>
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
