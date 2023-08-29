<!-- Header -->
<header id="header" class="alt">
    <h1 id="logo"><a href="main.php">
            <?php echo ($_SESSION['nn']); ?>
        </a></h1>
    <nav id="nav">
        <ul>
            <li class="submenu">
                <a href="#">메뉴</a>
                <ul>
                    <li><a href="main.php?page=head">본사</a></li>
                    <li><a href="main.php?page=site">현장</a></li>
                    <li><a href="main.php?page=transaction">거래</a></li>
                    <li><a href="main.php?page=subcontract">하도급</a></li>
                    <li><a href="main.php?page=leave">휴가 기안</a></li>
                    <li class="submenu" style="background: coral; color: white;">
                        <a href="#">시스템 관리</a>
                        <ul style="color: black;">
                            <li><a href="main.php?page=business_section">거래처 관리</a></li>
                            <li><a href="main.php?page=main_section">거래항목 관리</a></li>
                            <li><a href="main.php?page=sub_section">소분류 관리</a></li>
                            <li><a href="main.php?page=head_section">본사 통장 관리</a></li>
                            <li><a href="main.php?page=head_main_section">본사 거래항목 관리</a></li>
                            <li><a href="main.php?page=head_sub_section">본사 소분류 관리</a></li>
                        </ul>
                    </li>
                    <?php
                    if ($_SESSION['auth']) {
                        echo "<li style='background: pink; color: white;''><a href='main.php?page=request'>요청처리</a></li>";
                    }
                    ?>
                    <li><a href="apps/auth/logout.php">로그아웃</a></li>
                </ul>
            </li>
        </ul>
    </nav>
</header>