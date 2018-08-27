<?php
if(isset($_GET['hwid'])){
    $mysqli = new mysqli('mysql10.000webhost.com', 'a9443300_soundcl', 'playtime2', 'a9443300_soundcl');
    $hwid = mysqli_real_escape_string($mysqli, $_GET['hwid']);
    $query = "SELECT COUNT(*) FROM `uuid` WHERE `uuid` = '$hwid'";
    $result = $mysqli->query($query) or die($query . '<br />' . $mysqli->error);
    while ($row = mysqli_fetch_assoc($result)) {
        if ($row['COUNT(*)'] == 1) {
            echo 'truelikeurmumspot';
        } else {
            echo 'nopls';
        }
    }
} else {
    header('HTTP/1.1 404 Not Found', true, 404);
}