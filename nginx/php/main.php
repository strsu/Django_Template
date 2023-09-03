<?php session_start(); ?>
<!DOCTYPE HTML>
<html>
<?php
include("head.php");
require_once 'apps/api/api.php';
?>

<body class="index is-preload">
    <div class="container">
        <div class="sidebar">
            <?php include("nav.php"); ?>
        </div>
        <div class="content">
            <?php
                $page = $_GET['page'];

                if ($page == "resource") {
                    include("apps/resource/list.php");
                }
            ?>
        </div>
    </div>
</body>

</html>