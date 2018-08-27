<?php
include 'inc/header.php';
if(isset($_GET['download'])){
	$file = 'index.php';
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
			Miscellaneous!<br>
			Everything in this section is free, no user required, and "open source"<br>
			To get the source of the files in this section, simply append "?download" to the url<br>
			E.g. <a href="http://derpybooter.no-ip.org/misc/index.php?download" style="color: #FF66CC" target="_blank">http://derpybooter.no-ip.org/misc/index.php?download</a>
		</p>
	</body>
</html>