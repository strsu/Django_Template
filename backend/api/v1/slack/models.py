from django.db import models
from api.common.models import TimestampModel
from api.common import cache

from api.v1.user.models import User

import secrets
import string


class SlackAuth(TimestampModel):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        verbose_name="사용자 id",
    )

    slack_user_id = models.CharField("슬랙 사용자 ID", max_length=64, unique=True)

    def generate_auth_token(self):
        length = 16
        alphabet = string.ascii_letters + string.digits  # 대소문자 + 숫자
        token = "".join(secrets.choice(alphabet) for _ in range(length))

        cache.setKey(f"slack_{self.slack_user_id}", token, 600)

        return token

    def verify_token(self, token):
        cached_token = cache.getKey(f"slack_{self.slack_user_id}")
        if cached_token:
            if cached_token == token:
                return True
        return False

    def exist_token(self):
        cached_token = cache.getKey(f"slack_{self.slack_user_id}")
        if cached_token:
            return True
        return False
