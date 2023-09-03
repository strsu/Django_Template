function login() {

    let id = document.getElementById("id").value;
    let pw = document.getElementById("pw").value;
    let msg = document.getElementById("msg-box");

    if (id == "" || pw == "") {
        msg.style.display = "block";
        msg.innerText = "아이디/비밀번호 항목은 필수 정보입니다.";
        return;
    }

    $.ajax({
        url: 'apps/auth/login.php',
        data: {
            email: id,
            password: pw,
        },
        type: 'POST',
        dataType: 'json',
        success: function (result) {
            if (result.success == false) {
                msg.style.display = "block";
                msg.innerText = "조회결과가 없습니다.";
            } else {
                location.replace("main");
            }
        }, error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR.responseText);
        }
    });
}