from django.db import models
from api.common.models import TimestampModel
from api.common import cache

from django.contrib.auth import get_user_model

import secrets
import string


class SlackAuth(TimestampModel):
    user = models.ForeignKey(
        get_user_model(),
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


class SlackInteractivityHistory(TimestampModel):
    executor = models.ForeignKey(
        SlackAuth,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        verbose_name="사용자 id",
    )

    alerted_at = models.CharField("알림 발생 시점, unixtimestamp", max_length=20)
    executed_at = models.CharField("액션 수행 시점, unixtimestamp", max_length=20)
    action_prefix = models.CharField("액션 prefix", max_length=32)

    execute_result = models.CharField("수행 결과", max_length=256)

    class Meta:
        unique_together = [["action_prefix", "alerted_at"]]
