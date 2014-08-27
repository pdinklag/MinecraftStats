<?
    require_once('config.php');
    require_once('util.php');
?>
<!DOCTYPE html>
<html>
<head>
    <title><? echo($title); ?></title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<div id="last-update">
    The statistics were last updated 
    <?
        if(is_file($lastUpdateFile)) {
            $lastUpdate = unserialize(file_get_contents($lastUpdateFile));
            
            $delta = (time() - $lastUpdate);
            $deltaMinutes = (int)($delta / 60);
            
            if($delta >= 120) {
                echo("$deltaMinutes minutes ago.");
            } else if($delta >= 60) {
                echo("a minute ago.");
            } else {
                echo("$delta seconds ago.");
            }
        }
    ?>
</div>
<h1><? echo($title); ?></h1>
<?
    if(isset($_GET["stat"])) {
        require("view-stat.php");
    } else if(isset($_GET["player"])) {
        require("view-player.php");
    } else if(isset($_GET["raw"])) {
        require("view-player-raw.php");
    } else {
        require("view-awards.php");
    }
?>
<div id="foot-wrapper">
    &nbsp;
    <div id="foot">
        Written by Patrick Dinklage a.k.a. "pdinklag".
        <? if(isset($disclaimer)) { ?>
            <div id="disclaimer"><? echo($disclaimer); ?></div>
        <? } ?>
    </div>
</div>

<script type="text/javascript" src="jquery-2.1.1.min.js"></script>
<script type="text/javascript">
    $(".player img").load(function(event) {
        var img = event.target;
        var canvas = img.parentNode.getElementsByTagName("canvas")[0];
        
        var ctx = canvas.getContext('2d');
        ctx.imageSmoothingEnabled = false;
        ctx.drawImage(img, 8, 8, 8, 8, 0, 0, canvas.width, canvas.height);
    }).each(function() {
        if(this.complete) {
            $(this).load();
        }
    });
</script>

</body>
</html>
