<?php
if(strpos($_GET['key'], '123ovma78cj2n') !== false) {
	echo 'Added ' . $_GET['hwid'];
	file_put_contents('hwid.txt', "\r\n" . $_GET['hwid'], FILE_APPEND | LOCK_EX);
}
?>