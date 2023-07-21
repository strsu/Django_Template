import string
import random

from functools import wraps


def generate_random_string(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def get_authenticated_user(func):
    @wraps(
        func,
    )
    def inner(request, *args, **kwargs):
        user = request.user

        # 모든 모델에 사용자 정보를 전달합니다.
        kwargs["user"] = user

        return func(request, *args, **kwargs)

    return inner
