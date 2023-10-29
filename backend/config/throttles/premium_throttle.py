from rest_framework.throttling import UserRateThrottle

from config.exceptions.custom_exceptions import Code403Exception


class PremiumThrottle(UserRateThrottle):
    def __init__(self):
        """User에 따라 scope이 달라지기에, 생성자에서는 get_rate()를 수행하지 않도록 했습니다."""
        pass  # 생성자에서 기존의 scope을 구현하는 부분이 동작하지 않도록 비워둔다(pass).

    def allow_request(
        self, request, view
    ):  # allow_request라는 멤버함수 구현을 통해서 현재 이 요청을 허용/거부를 결정한다.
        # View에 premium_scope, light_scope가 있으면 동작한다.
        premium_scope = getattr(view, "premium_scope", None)
        light_scope = getattr(view, "light_scope", None)

        if request.user.is_anonymous:
            raise Code403Exception
        else:
            if request.user.auth:
                if not premium_scope:
                    return True
                self.scope = premium_scope  # premium_scope설정이 없다면, 제한을 두지 않습니다.
            else:
                if not light_scope:
                    return True
                self.scope = light_scope  # light_scope 설정이 없다면, 제한을 두지 않습니다.

            self.rate = self.get_rate()
        self.num_requests, self.duration = self.parse_rate(self.rate)

        return super().allow_request(request, view)
