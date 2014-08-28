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
<div id="nav">
    <a href="index.php">Awards</a>
    &nbsp;|&nbsp;
    <a href="?hof">Hall of Fame</a>
    &nbsp;|&nbsp;
    <a href="?stat=stat.playOneMinute">List of players</a>
    
    <?
        if(isset($_POST['me'])) {
            $name = $_POST['me'];
            $me = findPlayerUUIDByName($name);
            if($me !== FALSE) {
                setcookie('me', $me);
            } else {
                $formError = "Can't find " . htmlspecialchars($name) . "!"; //good thing I recently learned about cross-site-scripting!
                unset($me);
            }
        } else if(isset($_GET['notme'])) {
            setcookie('me', null);
        } else if(isset($_COOKIE['me'])) {
            $me = $_COOKIE['me'];
        }
    
        if(isset($me)) {
            ?>&nbsp;|&nbsp;<?
            echo(createPlayerWidget($me, 16));
            ?>
            <a class="notme" href="?notme">[X]</a>
            <?
        } else {
            ?>
                <form action="index.php" method="post">
                Player name: <input name="me" type="text" size="16"/> <input type="submit" value="Make shortcut"/>
                <?
                    if(isset($formError)) {
                        echo("<span class=\"error\">$formError</span>");
                    }
                ?>
                </form>
            <?
        }
    ?>
</div>
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
    } else if(isset($_GET["hof"])) {
        require("view-hof.php");
    } else {
        require("view-awards.php");
    }
?>
<div id="foot-wrapper">
    &nbsp;
    <div id="foot">
        Written by Patrick Dinklage a.k.a. "pdinklag".<br/>
        All times are CEST.
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
