<?php
$deny = array("176.53.69.121", "91.14.8.162", "96.44.189.102", "94.242.238.195", "65.183.151.13", "176.53.69.121");
if (in_array ($_SERVER['REMOTE_ADDR'], $deny)) {
   header("location: banned.php");
   exit();
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=Ubuntu:regular,bold&subset=Latin">
<link href="inc/style.css" rel="stylesheet" />
<title>Derpy Booter</title>
<!--[if lt IE 9]>
<script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
<![endif]-->
</head>
<body>
<?php include_once("analyticstracking.php") ?>
    
    <div class="Navigation">
        <div id="NavigationInside">
            <ul>
                <li><a href="index.php">Home&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></li>
                <li><a href="stats.php">Stats&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></li>
                <li><a href="hub.php">Hub&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></li>
                <li><a href="shells.php">Add Shells&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></li>
                <li><a href="resolvers.php">Resolvers</a>
                    <ul class="horizontal">
                        <li><a href="skype.php">Skype</a></li>
                        <li><a href="steam.php">Steam</a></li>
                        <li><a href="cloudflare.php">CloudFlare</a></li>
                    </ul>
                </li>
                <li><a href="faq.php">FAQ&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></li>
                <li><a href="misc/index.php">Misc&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></li>
            </ul>
        </div>
    </div>


<p style="text-align: center;">
    <a href="index.php"><img alt="" src="inc/images/logo.png" /></a></p>

<div id="startbar">
    <div id="win">

        <div id="menu">
            <div class="left-menu">
                <ul>
                    <li><a href="index.php">Home</a></li>
                    <li><a href="stats.php">Stats</a></li>
                    <li><a href="hub.php">Hub</a></li>
                    <li><a href="shells.php">Add shells</a></li>
                    <li><a href="hub.php">Hub</a></li>
                                        <li><a href="skype.php">Skype Resolver</a></li>
                                        <li><a href="steam.php">Steam Resolver</a></li>
                                        <li><a href="cloudflare.php">CloudFlare Resolver</a></li>
                    <li><a href="faq.php">FAQ</a></li>
                    <li><a href="misc/index.php">Misc</a></li>
                </ul>
                <form id="search" action="" name="prikitiw"><input type="text" placeholder="Search programs and files" /></form>
            </div> <!-- leftmenu -->
            <div class="clear"></div>
        </div> <!-- menu -->

        <div id="cont-win" title="Start">
            <div class="w1"></div><div class="w2"></div>
            <div class="clear"></div>
            <div class="w3"></div><div class="w4"></div>
            <div class="clear"></div>
        </div>

    </div> <!-- win -->

    <div id="list">

    </div> <!-- list -->
    <div class="clear"></div>
    </div> <!-- opened pilled -->

    

</div>
<div id="footer">
    <!-- Footer start -->
    <p class="footer"><strong>By <a href="http://www.hackforums.net/member.php?action=profile&uid=959991">Furry~</a></strong><br>
    I accept LR donations at U5088282</p>
    <!-- Footer end -->
</div>
</body>
</html>