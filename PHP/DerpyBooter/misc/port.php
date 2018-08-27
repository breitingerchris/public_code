<?php
include 'inc/header.php';
error_reporting(~E_ALL);
set_time_limit(0);
if(isset($_GET['download'])){
	$file = 'port.php';
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
		flush();
		readfile($file);
		exit;
	}
}
?>

<html>
	<body>
		<p style="text-align: center;">
			Port checker<br>
			This just checks to see if a port is open on the IP specified<br>
		</p>
		<br>
		<div class="box" align="center">
			<div class="box-content">
				<center>
					<form method="post">
						IP:<input type="text" id="ip" name="ip" placeholder="IP Address"><br>
						Single:<input type="radio" name="port" value="single"> <input type="text" id="single" name="single" SIZE="7" maxlength="5" placeholder="Single Port"><br>
						Range:<input type="radio" name="port" value="range"> <input type="text" id="start" name="start" SIZE="7" maxlength="5" placeholder="Start Port">-<input type="text" id="end" name="end" SIZE="7" maxlength="5" placeholder="End Port"><br>
						<input type="hidden" id="submit" name="submit">
						<input type="submit">
					</form>
				</center>
			</div>
		</div>
	</body>
</html>
<?php
if(isset($_POST['submit'])){
	$ip = $_POST['ip'];
	if(isset($_POST['port'])){
		if($_POST['port'] == 'single'){
			$port = $_POST['single'];
			$fp = fsockopen($ip , $port, $errno, $errstr, 1);
			if ($fp)
			{
				echo "<p class = \"success\">Port $port open </p>";
				fclose($fp);
			} else {
				echo "<p class = \"error\">Port $port closed</p>";
				fclose($fp);
			}
		}
		if($_POST['port'] == 'range'){
			$start = $_POST['start'];
			$end = $_POST['end'];
			for($port = $start; $port <= $end; $port++){
				$fp = fsockopen($ip , $port, $errno, $errstr, 1);
				if ($fp)
				{
					echo "<p class = \"success\">Port $port open </p>";
					fclose($fp);
				} else {
					echo "<p class = \"error\">Port $port closed</p>";
					fclose($fp);
				}
			}
		}
	}
}
?>