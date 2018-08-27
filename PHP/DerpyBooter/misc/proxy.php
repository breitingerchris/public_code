<?php
include 'inc/header.php';
set_time_limit(0);
if(isset($_GET['download'])){
    $file = 'proxy.php';
    if (file_exists($file)) {
        header('Content-Description: File Transfer');
        header('Content-Type: application/octet-stream');
        header('Content-Disposition: attachment; filename='.basename($file));
        header('Content-Transfer-Encoding: binary');
        header('Expires: 0');
        header('Cache-Control: must-revalidate');
        header('Pragma: public');
        header('Content-Length: ' . filesize($file));
        ob_clean();
        $file = 'proxy.php';flush();
        readfile($file);
        exit;
    }
}
?>

<html>
<body>
    <p style="text-align: center;">
    Proxy checker<br>
    Enter a list of 15 or less proxies<br>
    <b>The types are: 1 = transparent | 2 = anonymous | 3 = high anonymous.</b><br><br>
    <b><p class="error">This is only an example for others to use.<br> It will only check a list of 15 proxies!<br> No more than that is allowed to keep server resources low.<br> To remove this limit download the source and edit it yourself</p></b>
    <br>
    <div class="box" align="center">
    <h2>Check Proxies</h2>
        <div class="box-content">
            <center>
                <form method="post">
                    <textarea class="entryfield" name="proxy" cols=75 rows=6></textarea><br><br>
                    <input class="button" type="submit" name="Submit" value="Add Shells">
                </form>
            </center>
        </div>
    </div>
</body>
</html>

<?php
if(isset($_POST['proxy'])){
    $hosts = $_POST['proxy'];
    $hosts  = preg_replace("/(^[\r\n]*|[\r\n]+)[\s\t]*[\r\n]+/", "\n", $hosts);
    $hosts = explode("\n", $hosts);
    $count = count($hosts);
    if($count >= 15){
        die('Please enter only 15 or less shells');
    }
    $hosts  = array_unique($hosts);
    $testpage = "http://derpybooter.no-ip.org/";
    $proxies = $hosts;
    sort($hosts);
    foreach($proxies as $proxy)
    {
        $split = explode(':',$proxy);
        $ip = $split[0];
        $port = $split[1];
        $ch = curl_init('http://api.proxyipchecker.com/pchk.php');
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS,'ip='.$ip.'&port='.$port);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
        curl_setopt($ch, CURLOPT_HEADER, 0);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

        list($res_time, $speed, $country, $type) = explode(';', curl_exec($ch));
        if($type == 0){
            echo '<p class="error">'.$proxy.' does not work!</p>';
        }else{
             echo '<p class="success">'.$proxy.' Response time: '.$res_time.' seconds Country: '.$country.' -- Type: '.$type.'</p>';
        }
    }
}
?>
