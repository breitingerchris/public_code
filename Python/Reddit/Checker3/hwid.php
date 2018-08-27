<?php
if(isset($_GET['hwid'])){
    $mysqli = new mysqli('mysql1.000webhost.com', 'a5969019_checker', 'playtime2', 'a5969019_checker');
    $hwid = mysqli_real_escape_string($mysqli, $_GET['hwid']);
    $query = "SELECT COUNT(*) FROM `uuid` WHERE `uuid` = '$hwid'";
    $result = $mysqli->query($query) or die($query . '<br />' . $mysqli->error);
    while ($row = mysqli_fetch_assoc($result)) {
        if ($row['COUNT(*)'] == 1) {
            echo 'truelikeurmum';
        } else {
            echo 'nopls';
        }
    }
} else {
    header('HTTP/1.1 404 Not Found', true, 404);
}