<?php
if(strpos(file_get_contents("hwid.txt"), $_GET['pwid']) !== false) {
	echo md5($_GET['pwid']);
}
?>