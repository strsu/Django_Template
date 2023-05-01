class DefaultFault:
    REQUEST_SUCCESS = "요청 성공"
    REQUEST_FAIL = "요청 실패"


class UserFault:
    ## not found
    NOT_FOUND = {"message": "잘못된 요청입니다.", "code": 404, "status_code": 404}
    USRE_NOT_FOUND = {
        "message": "존재하지 않는 유저입니다. 다시 한 번 요청해주세요.",
        "code": 404,
        "status_code": 404,
    }

    PARAMETER_ERROR = {"message": "파라미터 오류입니다.", "code": 400, "status_code": 400}

    ## JWT
    JWT_EXPIRATION_ERROR_MSG = "계정이 활성화 상태가 아닙니다. 관리자에게 문의해주세요."
    JWT_LOGIN_ERROR_MSG = "아이디 또는 비밀번호가 잘못 입력 되었습니다. 확인 후 다시 입력해주세요."
