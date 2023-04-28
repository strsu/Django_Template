from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from config.settings.base import logger_info

from datetime import datetime
import pytz
import time
import base64
import logging
import json
import traceback

request_logger = logging.getLogger("middleware")
exception_logger = logging.getLogger("exception")


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.cached_request_body = None
        self.response_limit = 500
        # One-time configuration and initialization.

    def __call__(self, request):
        """
        @ 가장 먼저 호출되는 구간 -> process_request 역할?
        """
        self.cached_request_body = request.body
        self.process_request(request)
        response = self.get_response(request)
        """
        @ 가장 마지막에 호출되는 구간 ->process_response 역할?
        JJ: 여기서 return response가 없으면 view쪽에서 response가 None으로 넘어가나 보다. <- response되는 상위 middleware에서 문제 발생
        """
        self.process_response(request, response)
        return response

    def get_client_ip_address(self, request):
        req_headers = request.META
        x_forwarded_for_value = req_headers.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for_value:
            ip_addr = x_forwarded_for_value.split(",")[-1].strip()
        else:
            ip_addr = req_headers.get("REMOTE_ADDR")
        return ip_addr

    """http 요청 미들웨어"""

    def process_request(self, request):
        """
        정의되어 있으면 호출
            -> __call__ 때문엔지 실제로 호출되지 않는다.
        """
        request.start_time = time.time()

    # 장고가 view 를 호출하기 바로 직전에 불리는 훅이다
    # None 이나 HttpResponse 객체를 리턴해야 한다.
    # None 을 리턴하면, view 를 호출하고, HttpResponse 객체를 리턴하면,
    # 해당 HttpResponse 를 미들웨어로 다시 쏘아 올린다.
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        view_func:  django가 사용할 view function이다.
                    (It’s the actual function object, not the name of the function as a string.)
        view_args:  view에서 넘어오는 positional arguments 것
        view_kwargs:    view에서 넘어오는 dictionary of keyword arguments이다.

            view_args, view_kwargs 모두 첫 번째 인수인 request를 포함하지 않는다.
        """

        header_token = request.META.get("HTTP_AUTHORIZATION", None)
        if False and header_token is not None:
            # 여기서만 1000ms 가 소요된다...
            try:
                if "Basic" in header_token:
                    # id, pw로 로그인한 유저
                    credentials = header_token[len("Basic ") :].strip()
                    credentials = base64.b64decode(credentials).decode("utf-8")
                    username, password = credentials.split(":", 1)
                    user = authenticate(username=username, password=password)
                    print("@@", user)
                    request.user = user
                else:
                    # token으로 로그인한 유저
                    jwt_authentication = JWTAuthentication()
                    token = header_token[len("Bearer ") :].strip()
                    validated_token = jwt_authentication.get_validated_token(token)
                    user = jwt_authentication.get_user(validated_token)
                    request.user = user
            except Exception as e:
                """
                정말 이유를 모르겠지만, token이 잘못된경우 Circular Reference Error가 난다.
                이유를 모르겠다.
                그래서 처음에 사용자 인증이 안 된 경우 바로 response를 하는 방향으로,,
                """
                # print("@@", e.detail["detail"])
                response = Response(data={}, status=401)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = "application/json"
                response.renderer_context = {}
                return response

        logger_info.info(
            {
                "user": request.user.get_username(),
                "host": request.get_host(),
                "method": request.method,
                "full_path": request.get_full_path(),
                "path": request.path,
            }
        )

    """http 응답 미들웨어"""

    # response 가 템플릿을 반환하는 경우에만
    def process_template_response(self, request, response):
        """
        return reder 를 call 했는데, 이 부분에 안 옴...
        500 같은게 나면 여기로 오긴 한다.

        return None을 하면 response가 없다고 에러가 난다...
        """
        return response

    # view 가 exception 을 발생시키면 호출된다.
    def process_exception(self, request, exception):
        # 뷰 함수에서 예외가 발생한 경우 수행 할 작업
        return None

    def process_response(self, request, response):
        """
        정의되어 있으면 호출
            -> __call__ 때문엔지 실제로 호출되지 않는다.
        """
        try:
            seoul_tz = pytz.timezone("Asia/Seoul")
            seoul_time = datetime.now(seoul_tz)

            log_data = {
                "DATE": str(seoul_time),
                "REMODE_ADDR": self.get_client_ip_address(request)
                if "REMOTE_ADDR" in request.META.keys()
                else None,
                "PATH_INFO": request.get_full_path(),
                "STATUS_CODE": response.status_code,
                "METHOD": request.method,
                "QUERY_STRING": request.META["QUERY_STRING"]
                if "QUERY_STRING" in request.META.keys()
                else None,
                "USER_ID": request.user.uuid
                if str(request.user) != "AnonymousUser"
                else None,
                "USER_NAME": request.user.username
                if str(request.user) != "AnonymousUser"
                else None,
                "RESPONSE_TIME": round(time.time() - request.start_time, 8),
                "HTTP_USER_AGENT": request.META["HTTP_USER_AGENT"]
                if "HTTP_USER_AGENT" in request.META.keys()
                else None,
                "LEVEL": "INFO",
            }

            try:
                log_data["BODY"] = (
                    json.loads(self.cached_request_body)
                    if self.cached_request_body
                    else None
                )
            except Exception as e:
                log_data["BODY"] = (
                    str(self.cached_request_body) if self.cached_request_body else None
                )

            if (
                log_data["HTTP_USER_AGENT"]
                and "ELB-HealthChecker" in log_data["HTTP_USER_AGENT"]
            ):
                return response
            # 민감한 정보제거.
            if "token" in log_data["PATH_INFO"]:
                log_data["BODY"] = None
                log_data["RESPONSE"] = None

            if response.status_code in range(400, 500):
                log_data["LEVEL"] = "ERROR"
                exception_logger.error(log_data)
            elif response.status_code in range(500, 600):
                log_data["LEVEL"] = "CRITICAL"
                exception_logger.error(log_data)
            else:
                try:
                    log_data["RESPONSE"] = (
                        str(json.loads(response.content))[: self.response_limit]
                        if getattr(response, "content")
                        else None
                    )
                except:
                    pass
            request_logger.info(log_data)

        except Exception as e:
            print(f"[LOGGING ERROR]", e)
            print(request.method, request.get_full_path())

        return response
