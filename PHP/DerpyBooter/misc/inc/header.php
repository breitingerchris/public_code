<?php
$deny = array("176.53.69.121", "96.44.189.102", "65.183.151.13", "176.53.69.121");
if (in_array ($_SERVER['REMOTE_ADDR'], $deny)) {
   header("location: http://www.google.com/");
   exit();
} 
?>
<html>
<head>
<link href="inc/style.css" rel="stylesheet" />
<title>Derpy Booter</title>
</head>
<body>
<nav>
	<ul>
		<li><a href="index.php">Home</a></li>
		<li><a href="port.php">Port Scanner</a></li>
		<li><a href="minecraft.php">MC Skin Resolver</a></li>
        <li><a href="proxy.php">Proxy Checker</a></li>
		<li><a href="../index.php">Booter</a></li>
	</ul>
</nav>
<p style="text-align: center;">
	<a href="index.php"><img alt="" src="inc/logo.png" /></a></p>
	
</body>
</html>