<?php
ob_start();
require 'inc/db.php';
include 'inc/header.php';
?>

<html>
<head>
<script type="text/javascript">
var RecaptchaOptions = {
   theme : 'blackglass'
};
</script>
</head>
<body>
    <p style="text-align: center;">
        Don't register unless you have 50+ posts on HF<br>
        Once you registered you can PM me <a href="http://www.hackforums.net/private.php?action=send&uid=959991&subject=Derpy%20Booter&message=I%20registered%20on%20Derpy%20Booter%20please%20activate%20my%20account%20INSERT_ACCOUNT_NAME_HERE" style="color: #FF66CC" target="_blank">here</a>
<div class="loginWrapper">
    <?php
    require_once('inc/recaptchalib.php');
    $privatekey = "EDIT HERE";
    if (isset($_POST['registerBtn']))
    {
        $resp = recaptcha_check_answer ($privatekey,
        $_SERVER["REMOTE_ADDR"],
        $_POST["recaptcha_challenge_field"],
        $_POST["recaptcha_response_field"]);
        if (!$resp->is_valid) {
            die ("The reCAPTCHA wasn't entered correctly. Go back and try it again." .
            "(reCAPTCHA said: " . $resp->error . ")");
        } else {
            $username = $_POST['username'];
            $password = $_POST['password'];
            $email = $_POST['email'];
            $hf = $_POST['hf'];
            $query = "SELECT COUNT(*) FROM `users` WHERE `username` = '$username'";
            $result = $mysqli->query($query) or die($query.'<br />'.$mysqli->error);
            $row = mysqli_fetch_assoc($result);
            if (empty($username) || empty($password) || empty($email) || empty($hf))
            {
                die('<p class="error">Please fill in all fields</p>');
            }
            if ($email == 'sample@email.tst'){
                die('<p class="error">Fuck off with your crappy Acunetix</p>');
            }
            if ($row['COUNT(*)'] > 0)
            {
                die('<p class="error">Username is already taken</p>');
            }
            if (!ctype_alnum($username) || strlen($username) < 4 || strlen($username) > 15)
            {
                die('<p class="error">Username Must Be  Alphanumberic And 4-15 characters in length</p>');
            }
            if (!filter_var($email, FILTER_VALIDATE_EMAIL))
            {
                die('<p class="error">Email is invalid</p>');
            }
            if (!is_numeric($hf)) {
                die('<p class="error">Please only enter numbers in for your UID.</p>');
            }
            if($hf == 959991){
                die('<p class="error">You entered my UID...<br>It is hard to believe people are really this stupid...</p>');
            }
            $sha1pass = sha1($password);
            $query = "INSERT INTO `users` (`ID`, `username`,`password`,`email`,`uid`, `valid`) VALUES(NULL, '$username', '$sha1pass', '$email', '$hf', 0)";
            $mysqli->query($query) or die($query.'<br />'.$mysqli->error);
            echo '<p class="success">User has been registered.  Redirecting....</p><meta http-equiv="refresh" content="3;url=login.php">';
        }
    }
        ?>
        </div>
        <form action="" id="validate" class="form" method="POST">
            <fieldset>
                <div class="formRow" align="center">
                    <label for="login">Username:</label>
                    <div class="loginInput"><input type="text" name="username" class="validate[required]" id="username" maxlength="15"/></div>
                    <div class="clear"></div>
                    
                    <label for="pass">Password:</label>
                    <div class="loginInput"><input type="password" name="password" class="validate[required]" id="pass" /></div>
                    <div class="clear"></div>
                    
                    <label for="email">Email:</label>
                    <div class="loginInput"><input type="text" name="email" class="validate[required]" id="email" /></div>
                    <div class="clear"></div>
                    
                    <label for="hf">HackForums UID:</label>
                    <div class="loginInput"><input type="text" name="hf" class="validate[required]" id="hf" /></div>
                    <div class="clear"></div>
                    
                    <?php
                        require_once('inc/recaptchalib.php');
                        $publickey = "EDIT HERE";
                        echo recaptcha_get_html($publickey);
                    ?>
                    <input type="submit" class="large blue button" value="Register" name="registerBtn"/>
                    <div class="clear"></div>
                </div>
            </fieldset>
        </form>
        </div>
    </body>
</html>

