<?php
session_start();
$_SESSION['access'] = false;
#session_destroy(); // 세션 아이디의 삭제
echo ("<script>location.replace('../../index');</script>");
?>