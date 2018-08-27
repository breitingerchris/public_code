<?php

require 'inc/db.php';
include 'inc/header.php';

if (!($user->LoggedIn())) {
    if (isset($_POST['submit'])) {
        $username = $_POST['username'];
        $password = $_POST['password'];
        if (!ctype_alnum($username) || strlen($username) < 4 || strlen($username) > 15) {
            die('Username Must Be  Alphanumberic And 4-15 characters in length');
        }
        
        if (empty($username) || empty($password)) {
            die('Please fill in all fields');
        }
        
        $sha1pass = sha1($password);
        $query    = "SELECT COUNT(*) FROM `users` WHERE `username` = '$username' AND `password` = '$sha1pass' AND `valid` = 1";
        $result = $mysqli->query($query) or die($query . '<br />' . $mysqli->error);
        $row = mysqli_fetch_assoc($result);
        if ($row['COUNT(*)'] == 1) {
            $query = "SELECT `ID` FROM `users` WHERE `username` = '$username' AND `password` = '$sha1pass'";
            $result = $mysqli->query($query) or die($query . '<br />' . $mysqli->error);
            $row                  = mysqli_fetch_assoc($result);
            $_SESSION['username'] = $username;
            $_SESSION['ID']       = $row['ID'];
            $date                 = date('Y-m-d / H:i');
            $id                   = $_SESSION['ID'];
            $ip                   = $_SERVER['REMOTE_ADDR'];
            $query                = "INSERT INTO `iplogs` (`ID`, `userID`, `logged`, `date`) VALUES (NULL, '$id', '$ip', '$date')";
            $mysqli->query($query) or die($query . '<br />' . $mysqli->error);
            echo '<p class="success">Logged in.  Redirecting....</p><meta http-equiv="refresh" content="3;url=index.php">';
        } else {
            echo '<p class="error"> Either you entered the wrong information or the account is not activated';
        }
    }
} else {
    header('location: index.php');
}
?>
<html xmlns="http://www.w3.org/1999/xhtml">
    <body>
        <p style="text-align: center;">
            Welcome to the login page :D<br>
            Please enter the required fields to login<br>
        </p>
        <div class="container">
            <section class="main">
                <form class="login" action="" id="validate" class="form" method="POST">
                    <fieldset>
                        <div class="formRow" align="center">
                            <p class="clearfix">
                                <label for="username">Username</label>
                                <input type="text" name="username" id="username" placeholder="Username">
                            </p>
                            <p class="clearfix">
                                <label for="password">Password: </label>
                                <input type="password" name="password" id="password" placeholder="Password"> 
                            </p>
                            <p class="clearfix">
                                <input type="submit"  name="submit" value="Sign in">
                            </p>
                            <p class="clearfix">
                                <a href="register.php"><input type="button" value="Register" name="button" /></a>
                            </p>
                        </div>
                    </fieldset>
                </form>
            </section>
        </div>
    </body>
</html>
