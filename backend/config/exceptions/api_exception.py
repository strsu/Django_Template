from rest_framework import exceptions
from rest_framework.views import exception_handler, set_rollback
from rest_framework.response import Response

from django.db import connections

from config.exceptions.custom_exceptions import CustomException

from config.exceptions.exception_codes import STATUS_RSP_INTERNAL_ERROR

import logging
import traceback

logger = logging.getLogger("django")
exception_logger = logging.getLogger("exception")
logger_error = logging.getLogger("logstash_error")


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

    response = exception_handler(exc, context)

    """
        return이 None, HttpResponse 만 middleware에서 reqeust_exception이 호출된다.
        Response 객체로 넘어가면 middleware의 reqeust_exception이 호출되지 않음

        아무튼 그래서 밑에서 returne Response를 하니 loggingMiddleware에서 request_exception 함수가 호출 안 되는 것이다.
    """

    if response is not None:
        status_code = response.status_code

        msg = str(exc)
        errors = []

        if hasattr(exc, "detail"):
            msg = exc.detail

        if isinstance(exc, exceptions.ParseError):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.AuthenticationFailed):
            code = response.status_code
            msg = exc.detail
            if isinstance(msg, dict):
                if exc.detail.get("detail"):
                    msg = exc.detail.get("detail")
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
            """
            serializer에서 field가 없거나 type이 안 맞는 경우 발생
            """

            def extract_msg(error_dict, parent_attr=None):
                error = []
                nested_error = []
                for attr, detail in error_dict.items():
                    _attr = attr
                    if parent_attr:
                        _attr = f"{parent_attr}.{attr}"
                    if isinstance(detail, list):
                        error.append(
                            {
                                "code": detail[0].code,
                                "message": detail[0],
                                "attr": _attr,
                            }
                        )
                    elif isinstance(detail, dict):
                        nested_error += extract_msg(detail, _attr)
                    else:
                        error.append(
                            {
                                "code": "error",
                                "message": detail,
                                "attr": _attr,
                            }
                        )

                return error + nested_error

            code = response.status_code
            msg = exc.detail
            errors = extract_msg(exc.detail)
        elif isinstance(exc, CustomException):
            msg = exc.detail
            code = exc.detail.code
            status_code = code
        else:
            code = response.status_code
            # msg = "unknown error"

        if not errors:
            errors.append({"message": msg})

        status_code = status_code
        data = {"errors": errors, "code": code}

        ## 위 handler에서 exception내용이 response에 들어가는 것 같다.
        # response.data.pop("status_code", None)
        set_rollback()
        return Response(data, status=status_code)

    else:
        """일반적으로 Err가 발생하면 이쪽으로 빠진다."""
        msg = {"errors": [{"message": str(exc)}], "code": 500}

        # context["request"]["_data"] = {
        #     **context["request"]["_data"],
        #     "exception": {
        #         **msg,
        #         status_code: 500,
        #     },
        # }
        set_rollback()
        return Response(msg, status=500)
