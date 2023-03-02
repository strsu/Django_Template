from datetime import datetime

from rest_framework.views import exception_handler
from rest_framework import exceptions
from rest_framework.response import Response

from config.exceptions.custom_exceptions import (
    CustomDictException,
    CustomParameterException,
)
from config.settings import logger
from config.exceptions.exception_codes import STATUS_RSP_INTERNAL_ERROR


def custom_exception_handler(exc, context):
    logger.error(f"[CUSTOM_EXCEPTION_HANDLER_ERROR]")
    logger.error(f"[{datetime.now()}]")
    logger.error(f"> exc")
    logger.error(f"{exc}")
    logger.error(f"> context")
    logger.error(f"{context}")

    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, exceptions.ParseError):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.AuthenticationFailed):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.NotAuthenticated):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.PermissionDenied):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.NotFound):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.MethodNotAllowed):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.NotAcceptable):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.UnsupportedMediaType):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.Throttled):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.ValidationError):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, CustomParameterException):
            code = CustomParameterException.default_code
            msg = CustomParameterException.default_detail
        elif isinstance(exc, CustomDictException):
            """
            APIException dictionary instance process
            For Localization Error Control

            아래와 같은 형태 필요
            STATUS_RSP_INTERNAL_ERROR = {
                'code': 'internal-error',
                'default_message': 'unknown error occurred.',
                'lang_message': {
                    'ko': '알 수 없는 오류.',
                    'en': 'unknown error occurred.',
                }
            }

            CustomDictException(STATUS_RSP_INTERNAL_ERROR, {"키": "내용", "키": "내용"}) 으로 추가 가능
            code 부분을 추가적인 내용을 넣는 방식으로 사용
            """

            print(exc.detail)

            code = exc.detail.get("status_code")

            if hasattr(context["request"], "LANGUAGE_CODE"):
                language_code = context["request"].LANGUAGE_CODE
                msg = exc.detail.get("lang_message").get(language_code)
            else:
                msg = exc.detail.get("default_message")

            if exc.args[1:]:
                for key, val in exc.args[1].items():
                    response.data[key] = val

            response.data.pop("default_message", None)
            response.data.pop("lang_message", None)
        else:
            code = response.status_code
            msg = "unknown error"

        response.status_code = 200
        response.data["code"] = code
        response.data["message"] = msg
        response.data["data"] = None

        response.data.pop("detail", None)

        return response
    else:
        msg = {"message": str(exc), "code": 500}

        return Response(msg, status=500)
