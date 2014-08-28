<?
    /**
     * Viewing raw data of a specific player.
     *
     * Included by index.php when $_GET['raw'] is set.
     */
    $playerId = $_GET["raw"];
    if(isset($players[$playerId])) {
        $player = $players[$playerId];

        //Load player JSON
        $jsonFile = "$rawDataDir/$playerId.json";
        if(is_file($jsonFile)) {
            $json = json_decode(file_get_contents($jsonFile), true);
        } else {
            die("No data file.");
        }
    } else {
        die("Unknown player.");
    }
    
    //Count stats
    $blockStats = [];
    $otherStats = [];
    
    foreach($json as $key => $value) {
        if(strpos($key, 'stat.craftItem.') === 0) {
            $id = substr($key, 15);
            $blockStats[$id]['craft'] = $value;
        } else if(strpos($key, 'stat.useItem.') === 0) {
            $id = substr($key, 13);
            $blockStats[$id]['use'] = $value;
        } else if(strpos($key, 'stat.mineBlock.') === 0) {
            $id = substr($key, 15);
            $blockStats[$id]['mine'] = $value;
        } else if(strcmp($key, 'achievement.exploreAllBiomes') === 0) {
            $otherStats[$key] = implode(', ', $value['progress']);
        } else {
            $otherStats[$key] = $value;
        }
    }
    
    //Sort stats
    ksort($otherStats);
    ksort($blockStats);
?>
<div id="header">
    <? echo(createPlayerWidget($playerId, 64)); ?>
</div>
<div id="listing-wrapper">
    <div class="listing">
        <p class="date">Last online: <? echo(formatDate($player['date'])); ?></p>
        <p>Raw craft, use/place and mine/destroy statisitcs:</p>
        <table class="listing">
            <colgroup>
                <col style="width:40%;"/>
                <col style="width:20%;"/>
                <col style="width:20%;"/>
                <col style="width:20%;"/>
            </colgroup>
            <tbody>
                <tr>
                    <th>Item/Block ID</th>
                    <th>Crafted</th>
                    <th>Used/Placed</th>
                    <th>Mined/Destroyed</th>
                </tr>
                <?
                    foreach($blockStats as $id => $stats) {
                        ?>
                            <tr>
                            <td><? echo($id); ?></td>
                            <td><? echo(safeGet('craft', $stats, 0)); ?></td>
                            <td><? echo(safeGet('use', $stats, 0)); ?></td>
                            <td><? echo(safeGet('mine', $stats, 0)); ?></td>
                            </tr>
                        <?
                    }
                ?>
            </tbody>
        </table>
        <hr />
        <p>Miscellaneous raw statistics:</p>
        <table class="listing">
            <colgroup>
                <col style="width:40%;"/>
                <col style="width:60%;"/>
            </colgroup>
            <tbody>
                <tr>
                    <th>Stat</th>
                    <th>Value</th>
                </tr>
                <?
                    foreach($otherStats as $key => $value) {
                        ?>
                            <tr>
                            <td><? echo($key); ?></td>
                            <td><? echo($value); ?></td>
                            </tr>
                        <?
                    }
                ?>
            </tbody>
        </table>
    </div>
</div>
