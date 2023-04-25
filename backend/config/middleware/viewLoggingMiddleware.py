from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from config.settings.base import logger_info

from re import sub
import base64


class viewLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        """
        @ 가장 먼저 호출되는 구간 -> process_request 역할?
        """
        print("###__call__: before")
        response = self.get_response(request)
        """
        @ 가장 마지막에 호출되는 구간 ->process_response 역할?
        JJ: 여기서 return response가 없으면 view쪽에서 response가 None으로 넘어가나 보다. <- response되는 상위 middleware에서 문제 발생
        """
        print("###__call__: after")
        return response

    """http 요청 미들웨어"""

    def process_request(self, request):
        """
        정의되어 있으면 호출
            -> __call__ 때문엔지 실제로 호출되지 않는다.
        """
        print("###process_request")

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
        print("###process_view")

        header_token = request.META.get("HTTP_AUTHORIZATION", None)
        if header_token is not None:
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
        print(
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
        print("###process_template_response")
        return response

    # view 가 exception 을 발생시키면 호출된다.
    def process_exception(self, request, exception):
        print("###process_exception")
        # 뷰 함수에서 예외가 발생한 경우 수행 할 작업
        if isinstance(exception, Exception):
            # MyException 예외를 처리하는 경우 로깅
            logger_info.info("Handling MyException")
        return None

    def process_response(self, request, response):
        """
        정의되어 있으면 호출
            -> __call__ 때문엔지 실제로 호출되지 않는다.
        """
        print("###process_response")
        return response
