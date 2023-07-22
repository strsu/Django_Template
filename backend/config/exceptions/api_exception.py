from rest_framework.views import exception_handler
from rest_framework import exceptions
from rest_framework.response import Response

from config.exceptions.custom_exceptions import (
    CustomException,
    CustomDictException,
    CustomParameterException,
)
from config.settings.base import logger_error
from config.exceptions.exception_codes import STATUS_RSP_INTERNAL_ERROR

import logging
import traceback

logger = logging.getLogger("django")
exception_logger = logging.getLogger("exception")


def custom_exception_handler(exc, context):
    message = {"message": str(exc)}

    if "view" in context:
        if "head" in context["view"].__dict__:
            message["head"] = context["view"].__dict__["head"].__dict__
        if "headers" in context["view"].__dict__:
            message["headers"] = context["view"].__dict__["headers"]
        if "request" in context["view"].__dict__:
            message["request"] = context["view"].__dict__["request"]
        if "args" in context["view"].__dict__:
            message["args"] = context["view"].__dict__["args"]
        if "kwargs" in context["view"].__dict__:
            message["kwargs"] = context["view"].__dict__["kwargs"]

        logger_error.error(message)

    message["trackback"] = traceback.format_exc()
    exception_logger.error(traceback.format_exc())

    logger.info(traceback.format_exc())

    response = exception_handler(exc, context)

    if response is not None:
        status_code = response.status_code

        msg = str(exc)

        if hasattr(exc, "detail"):
            msg = exc.detail

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
        elif isinstance(exc, CustomException):
            msg = exc.detail.get("message")
            code = exc.detail.get("code")
            status_code = int(exc.detail.get("status_code"))
        else:
            code = response.status_code
            msg = "unknown error"

        response.status_code = status_code
        response.data = {"message": msg, "code": code}

        ## 위 handler에서 exception내용이 response에 들어가는 것 같다.
        # response.data.pop("status_code", None)

        return response
    else:
        """일반적으로 Err가 발생하면 이쪽으로 빠진다."""
        msg = {"message": str(exc), "code": 500}
        return Response(msg, status=500)
