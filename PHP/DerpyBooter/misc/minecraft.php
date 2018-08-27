<?php
include 'inc/header.php';
if(isset($_GET['download'])){
	$file = 'minecraft.php';
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
			Minecraft Skin Resolver!<br>
			This one has gone a little untested as I don't really know much about Minecraft and it's skins<br>
			However, it should work (I think)<br>
		</p>
		<br>
		<div align="center">
			<form method="post">
				<input type="hidden" id="submit" name="submit" value="1">
				<input type="text" id="username" name="username" placeholder="MineCraft Username">
				<input type="submit">
			</form>
		</div>
	</body>
</html>

<?php
if(isset($_POST['submit'])){
	$skin = '<img src="http://minecraft.net/skin/'.$_POST['username'].'.png">';
	echo '<br><p class="text">'.$skin.'</p>';
}
?>