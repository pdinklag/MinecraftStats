<?
    /**
     * Viewing search results.
     *
     * Included by index.php when $searchResults contains more than one item.
     */
    
    //Load HOF
    if(is_file($hofFile)) {
        $hof = unserialize(file_get_contents($hofFile));
    } else {
        $hof = [];
    }
?>
<div id="header">
    Search results
</div>
<div id="listing-wrapper">
    <div class="listing">
        <div>
            Your search for <span id="searchterm"><? echo(htmlspecialchars($search)); ?></span> yielded <? echo(count($searchResults)); ?> results:
        </div>
        <div id="searchresults-wrapper">
            <div id="searchresults">
            <?
            foreach($searchResults as $uuid) {
                ?>
                <div class="searchresult">
                <? echo(createPlayerWidget($uuid, 16)); ?>
                </div>
                <?
            }
            ?>
            </div>
        </div>
    </div>
</div>
