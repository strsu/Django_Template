from rest_framework.views import exception_handler
from rest_framework import exceptions
from rest_framework.response import Response

from django.db import connections

from config.exceptions.custom_exceptions import (
    CustomException,
    CustomDictException,
    CustomParameterException,
    Code400Exception,
    Code403Exception,
)

from config.exceptions.exception_codes import STATUS_RSP_INTERNAL_ERROR

import logging
import traceback

logger = logging.getLogger("django")
exception_logger = logging.getLogger("exception")
logger_error = logging.getLogger("logstash_error")


def set_rollback():
    for db in connections.all():
        if db.settings_dict["ATOMIC_REQUESTS"] and db.in_atomic_block:
            db.set_rollback(True)


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

    """
        return이 None, HttpResponse 만 middleware에서 reqeust_exception이 호출된다.
        Response 객체로 넘어가면 middleware의 reqeust_exception이 호출되지 않음

        아무튼 그래서 밑에서 returne Response를 하니 loggingMiddleware에서 request_exception 함수가 호출 안 되는 것이다.
    """

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
        if isinstance(exc, Code400Exception):
            msg = exc.detail
            code = Code400Exception.default_code
            if not msg:
                msg = Code400Exception.default_detail
            status_code = Code400Exception.default_code
        if isinstance(exc, Code403Exception):
            msg = exc.detail
            code = Code403Exception.default_code
            if not msg:
                msg = Code403Exception.default_detail
            status_code = Code403Exception.default_code
        elif isinstance(exc, CustomException):
            msg = exc.detail.get("message")
            code = exc.detail.get("code")
            status_code = int(exc.detail.get("status_code"))
        else:
            code = response.status_code
            msg = "unknown error"

        status_code = status_code
        data = {"message": msg, "code": code}

        ## 위 handler에서 exception내용이 response에 들어가는 것 같다.
        # response.data.pop("status_code", None)
        set_rollback()
        return Response(data, status=status_code)

    else:
        """일반적으로 Err가 발생하면 이쪽으로 빠진다."""
        msg = {"message": str(exc), "code": 500}

        # context["request"]["_data"] = {
        #     **context["request"]["_data"],
        #     "exception": {
        #         **msg,
        #         status_code: 500,
        #     },
        # }
        return Response(msg, status=500)
