<?php
session_start();
if (isset($_SESSION['access'])) {
	if ($_SESSION['access']) {
		echo ("<script>location.replace('main.php');</script>");
	}
}
?>
<!DOCTYPE HTML>
<html>

<head>
	<title>장고</title>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
	<link rel="stylesheet" href="assets/css/login.css" />
</head>

<body class="index is-preload login-outer">
	<div class="login-inner">
		<div class="login">
			<input type="text" id="id" name="id" placeholder="ID" />
			<input type="password" id="pw" name="pw" placeholder="PASSWORD" />
			<div id="msg-box"></div>
			<button onclick="login()">Login</button>
		</div>
	</div>

    <script src="apps/auth/login.js"></script>

</body>

</html>