<?php
require_once "../vendor/autoload.php";

use anytizer\relay;

$_GET = [];
$_POST = [];

$relay = new relay();
$relay->force_post();
$relay->headers([
    "X-Protection-Token" => ""
]);

/**
 * Different endpoints
 */
#$json = $relay->fetch("http://localhost:5000/api/missing/list");
#$json = $relay->fetch("http://localhost:5000/api/amenities/list");
$json = $relay->fetch("http://localhost:5000/api/associates/list");

echo $json;
