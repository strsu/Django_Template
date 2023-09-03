<?php
if (isset($_SESSION['access'])) {
    if ($_SESSION['access'] == false) {
        echo ("<script>location.replace('index.php');</script>");
    }
} else {
    echo ("<script>location.replace('index.php');</script>");
}
?>

<head>
    <title>장고</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
    <link rel="stylesheet" href="assets/css/main.css" />
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
</head>