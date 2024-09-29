from rest_framework.exceptions import APIException


class CustomException(APIException):
    pass


class Code400Exception(APIException):
    status_code = 400
    default_detail = "사용자 요청 실패"
    default_code = 400


class Code403Exception(APIException):
    status_code = 403
    default_detail = "접근 권한이 없습니다."
    default_code = 403


class Code404Exception(APIException):
    status_code = 404
    default_detail = "자원을 찾을 수 없습니다."
    default_code = 404


class CustomDictException(APIException):
    status_code = 500
    default_detail = "unknown error."
    default_code = "unknown-error"


class CustomParameterException(APIException):
    status_code = 500
    default_detail = "요청 파라미터가 잘못되었습니다"
    default_code = 400
