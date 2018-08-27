<?php
if($_GET['key'] == '123ovma78cj2n') {
	echo 'Removed ' . $_GET['hwid'];
	file_put_contents('hwid.txt', str_replace($_GET['hwid'], "", file_get_contents("hwid.txt")), LOCK_EX);
}
?>