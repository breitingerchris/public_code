<?php
require 'functions.php';
require 'CURL.php';
$user = new user;

$DB_NAME = 'booter';
$DB_HOST = 'localhost';
$DB_USER = '';
$DB_PASS = '';
$mysqli = new mysqli($DB_HOST, $DB_USER, $DB_PASS, $DB_NAME);
?>