from django.conf import settings

from api.v1.slack.services.slack_manager import SlackManager

from api.v1.slack.models import SlackAuth
from .annoy.electron_action import ElectronAction

import logging

logger = logging.getLogger("debug")


class AnnoyApp:
    """
    AnnoyApp은 여러가지 임무를 수행하는 봇
    따라서 action_id에 따라 해당하는 action을 수행하는 역할을 한다.
    """

    """
    About Action

    여러개의 액션을 지닌경우, 해당 block에 들어가는 모든 action이 한번에 오지 않는다.
    
    """
    APP_ID = settings.SLACK["annoy"]["app_id"]
    TOKEN = settings.SLACK["annoy"]["token"]
    OAUTH_TOKEN = settings.SLACK["annoy"]["oauth_token"]

    def __init__(self, channel: str, user: SlackAuth):
        self.slack_manager = SlackManager(channel, self.OAUTH_TOKEN)
        self.user = user

    def actions(self, actions: list, state: dict, thread_ts: str):
        """
        동일한 기능에 대해 action_id를 여러개 정의헤야 하기 때문에!!
        반드시 `prefix__` 로 action_id를 정의해야 한다!!!
        """
        for action in actions:
            action_id: str = action.get("action_id")

            if action_id.startswith(ElectronAction.ACTION_PREFIX):
                actor = ElectronAction(self.user, self.slack_manager)
                actor.resolve(action, state, thread_ts)
            else:
                # 정의되지 않았거나, 정의하면 안되는
                pass
