from rest_framework.exceptions import APIException


class CustomException(APIException):
    pass


class CustomDictException(APIException):
    status_code = 500
    default_detail = "unknown error."
    default_code = "unknown-error"


class CustomParameterException(APIException):
    status_code = 500
    default_detail = "요청 파라미터가 잘못되었습니다"
    default_code = 400
