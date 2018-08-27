<?php
include 'inc/header.php';

if (isset($_POST['submit'])) {
    if (isset($_POST['username'])) {
        $browser  = $_SERVER['HTTP_USER_AGENT'];
        $username = $_POST['username'];
        
        // API #1
        $url = 'http://skyperesolver.eu5.org/';
        $fields   = array(
            'username' => urlencode($username),
            'submit' => 'Resolve+Skype+Username%21'
        );
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_HEADER, 0);
        curl_setopt($ch, CURLOPT_TIMEOUT, 8);
        curl_setopt($ch, CURLOPT_USERAGENT, '$browser)');
        curl_setopt($ch, CURLOPT_POSTFIELDS, $fields);
        $result = curl_exec($ch);
        preg_match('#(.*?)</strong><br />#', $result, $match);
        
        // API #2
        $url = 'http://resolver.be/';
        $fields   = array(
            'skypen' => urlencode($username),
            'sub' => 'Resolve%21'
        );
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_HEADER, 0);
        curl_setopt($ch, CURLOPT_TIMEOUT, 8);
        curl_setopt($ch, CURLOPT_USERAGENT, '$browser)');
        curl_setopt($ch, CURLOPT_POSTFIELDS, $fields);
        $result = curl_exec($ch);
        preg_match('#<center>(.*?):#', $result, $match1);
    } else {
        echo 'Please fill in all the fields';
    }
} else {
    
}
?>
<html>
    <body>
        <p style="text-align: center;">
            Skype Resolver!<br>
            Enter Skype name<br>
            You might have to try a few times<br>
        </p>
        <br>
        <div align="center">
            <form method="post">
                <input type="hidden" id="submit" name="submit" value="1">
                <input type="text" id="username" name="username" placeholder="Skype Name">
                <input type="submit">
            </form>
        </div>
        <p style="text-align: center;">
            <?php
            if(isset($match) && isset($match1)){
                if($match[1] == $match1[1]){
                    echo '<p class="text"> API #1 and #2 found the IP <a href="http://whatismyipaddress.com/ip/'.$match[1].'" target="_blank" style="color: #66FF66">'.$match[1].'</a></p>';
                } else {
                    if(!empty($match[1])) {
                        echo '<p class="text">API #1 IP found: <a href="http://whatismyipaddress.com/ip/'.$match[1].'" target="_blank" style="color: #66FF66">'.$match[1].'</a></p>';
                    } else {
                        echo '<p class="error"> API #1 did not return an IP</p>';
                    }
                    if(!empty($match1[1])) {
                        echo '<p class="text">API #2 IP found: <a href="http://whatismyipaddress.com/ip/'.$match1[1].'" target="_blank" style="color: #66FF66">'.$match1[1].'</a></p>';
                    } else {
                        echo '<p class="error"> API #2 did not return an IP</p>';
                    }
                }
            }
            ?>
        </p>
    </body>
</html>
