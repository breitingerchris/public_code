<?php
if (!empty($_GET['l']) && !empty($_GET['serial'])) {
	if (strpos(file_get_contents('./ser.txt'), $_GET['serial']) !== false) {
		if (strpos(file_get_contents('./usrs.txt'), $_GET['l']) === false) {
			$f = fopen("./usrs.txt", "a") or die("Unable to open file!");
			fwrite($f, $_GET['l'] . "\n");
			$f = fopen("./ser.txt", "w") or die("Unable to open file!");
			fwrite($f, "");
		}
	}
	
	if (strpos(file_get_contents('./usrs.txt'), $_GET['l']) !== false) {
		$f = fopen("./log.txt", "a") or die("Unable to open file!");
		fwrite($f, $_GET['user'] . ' - ' . $_SERVER['REMOTE_ADDR'] . "\n");
		print $_GET['l'];
	}
}
else 
{
	print 'man fug ov';
}
?>