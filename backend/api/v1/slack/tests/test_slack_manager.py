from django.test import TestCase
from django.contrib.auth import get_user_model

from api.v1.slack.services.slack_manager import SlackManager
from api.v1.slack.models import SlackAuth

import time

# python manage.py test api.v1.slack.tests.test_slack_manager


class SlackManagerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test", email="test", password="test"
        )
        cls.slack_auth = SlackAuth.actives.create(user=cls.user, slack_user_id="")

    def tearDown(self):
        pass

    def test_슬랙_알림_보내기(self):

        channel = ""
        token = ""

        slack_manager = SlackManager(channel, token)
        thread_ts = slack_manager.post_message(text="안녕하세요")

        time.sleep(5)

        slack_manager.update_message(text="수정하였습니다", thread_ts=thread_ts)
