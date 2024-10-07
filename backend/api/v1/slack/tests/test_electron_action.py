from django.test import TestCase
from django.contrib.auth import get_user_model

from api.v1.slack.services.interativity.annoy.electron_action import ElectronAction
from api.v1.slack.services.slack_manager import SlackManager

from api.v1.slack.models import SlackAuth


# python manage.py test api.v1.slack.tests.test_electron_action


class AccountConcurrencyTest(TestCase):

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
        electron_action = ElectronAction(self.slack_auth, slack_manager)

        electron_action.alert({})
