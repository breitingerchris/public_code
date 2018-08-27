<?php

include 'inc/db.php';
include 'inc/header.php';
if (!($user->LoggedIn())) {
    header('location: login.php');
    die();
}
$query = "UPDATE counter SET counter = counter + 1";
$mysqli->query($query) or die($query . '<br />' . $mysqli->error);
?>


<html>
    <body>
        <p style="text-align: center;">
            Welcome to Derpy Booter!<br>
            This is a /free/, community booter<br>
            New users start out with 15 seconds boot time, but if you submit more shells you get an extra 15 seconds, so the more shells you add, the more time you get
                </p>
    </body>
</html>