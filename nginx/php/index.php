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
        <div class="login-title">
            <svg data-v-a6550d76="" xmlns="http://www.w3.org/2000/svg" width="145" height="24" transform="scale(1.1)"
                viewBox="0 0 130 21">
                <g fill="none" fill-rule="evenodd">
                    <g fill="#ff7133">
                        <g>
                            <path
                                d="M43.516 5.134c3.14 0 4.169.244 5.012.38.396.054.528.188.528.568v1.73c0 .298-.239.542-.528.542h-5.38c-1.53 0-2.083.54-2.083 2.327v2.921h7.146c.291 0 .527.244.527.541v1.947c0 .298-.236.542-.527.542h-7.146v3.488c0 1.787.553 2.327 2.083 2.327h5.38c.29 0 .528.244.528.542v1.73c0 .38-.132.515-.528.568-.843.137-1.872.38-5.012.38-3.428 0-6.09-.948-6.09-5.547v-9.44c0-4.598 2.662-5.546 6.09-5.546zm33.048 0c4.351 0 7.517 2.489 7.517 8.442v3.65c0 5.953-3.166 8.441-7.517 8.441-4.35 0-7.516-2.488-7.516-8.44v-3.651c0-5.953 3.165-8.442 7.516-8.442zm18.33 0c4.352 0 7.516 2.489 7.516 8.442v3.65c0 5.953-3.164 8.441-7.515 8.441-4.352 0-7.518-2.488-7.518-8.44v-3.651c0-5.953 3.166-8.442 7.518-8.442zM3.139 5.35c.29 0 .528.216.528.515v7.465h7.49V5.866c0-.299.237-.515.527-.515h2.61c.29 0 .528.216.528.515V24.91c0 .296-.237.54-.527.54h-2.611c-.29 0-.527-.244-.527-.54v-8.278h-7.49v8.278c0 .296-.238.54-.528.54H.528c-.29 0-.528-.244-.528-.54V5.866c0-.299.237-.515.527-.515zm23.11-.217c1.143.018 2.942.326 3.554 2.759l4.326 16.962c0 .054.026.108.026.134 0 .272-.211.462-.474.462h-2.797c-.236 0-.448-.217-.5-.462l-1.214-5.137h-6.065L21.89 24.99c-.053.245-.264.462-.502.462h-2.794c-.264 0-.476-.19-.476-.462 0-.026.026-.08.026-.134l4.326-16.962c.633-2.514 2.532-2.76 3.665-2.76zm82.704.217c.422 0 .792.27.975.65l3.984 8.277c.132.244.183.378.29.378.105 0 .157-.134.29-.378l3.982-8.277c.185-.38.554-.65.975-.65h2.162c.582 0 1.057.486 1.057 1.082v18.611c0 .272-.211.407-.45.407h-2.662c-.238 0-.424-.27-.424-.541V12.33c0-.19-.025-.27-.078-.27-.026 0-.08.08-.133.163l-2.53 5.166c-.16.298-.503.459-.845.459h-2.663c-.343 0-.685-.161-.845-.459l-2.557-5.166c-.053-.083-.106-.164-.132-.164-.053 0-.079.081-.079.27v12.58c0 .271-.184.542-.422.542h-2.664c-.237 0-.448-.135-.448-.407V6.434c0-.597.474-1.083 1.055-1.083zm-44.785 0c.765 0 1.398.325 1.398 1.029v1.568c0 .378-.159.784-.369 1.11L56.97 21.69c-.08.107-.107.216-.107.297 0 .107.053.162.238.162h8.123c.29 0 .527.19.527.487v2.273c0 .296-.237.54-.527.54H53.697c-.765 0-1.344-.27-1.344-1v-1.488c0-.325.08-.622.343-1.028l8.36-12.85c.053-.081.078-.162.078-.242 0-.137-.079-.217-.262-.217h-7.333c-.29 0-.5-.19-.5-.487V5.866c0-.298.21-.516.5-.516zm12.397 3.058c-2.584 0-3.823 1.595-3.823 5.167v3.65c0 3.572 1.239 5.166 3.823 5.166 2.585 0 3.824-1.594 3.824-5.166v-3.65c0-3.572-1.24-5.167-3.824-5.167zm18.33 0c-2.585 0-3.824 1.595-3.824 5.167v3.65c0 3.572 1.24 5.166 3.825 5.166 2.583 0 3.822-1.594 3.822-5.166v-3.65c0-3.572-1.239-5.167-3.822-5.167zm-68.758-.11c-.263 0-.342.11-.421.433l-1.9 8.035h4.642l-1.899-8.035c-.079-.324-.158-.433-.422-.433z"
                                transform="translate(-135 -23) translate(135 18)"></path>
                        </g>
                    </g>
                </g>
            </svg>
            <div>자원관리</div>
        </div>
        <div class="login">
            <input type="text" id="id" name="id" placeholder="아이디" />
            <input type="password" id="pw" name="pw" placeholder="비밀번호" />
            <div id="msg-box"></div>
            <button onclick="login()">로그인</button>
        </div>
    </div>

    <script src="apps/auth/login.js"></script>

</body>

</html>