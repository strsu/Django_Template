<?php session_start(); ?>
<!DOCTYPE HTML>
<html>
<?php
include("head.php");
?>

<body class="index is-preload">
    <div id="page-wrapper">
        <?php include("nav.php"); ?>
    </div>

    <div class="content">
        <?php
        $page = $_GET['page'];

        if ($page == "site") {
            include("apps/site/site.php");
        }
        ?>
    </div>


</body>

</html>