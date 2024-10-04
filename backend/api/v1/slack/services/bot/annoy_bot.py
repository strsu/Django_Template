from api.v1.slack.services.slack_manager import SlackManager

from api.v1.slack.models import SlackAuth
from .bot import Bot

import logging

logger = logging.getLogger("debug")


class AnnoyBot(Bot):

    TOKEN = ""
    BOT_TOKEN = ""

    def __init__(self, channel: str, user: SlackAuth):
        self.slack_manager = SlackManager(channel, self.BOT_TOKEN)
        self.user = user

    def actions(self, actions: list, thread_ts: str):
        for action in actions:
            action_id = action.get("action_id")
            type = action.get("type")

            if action_id is None:
                msg = f"확인 할 수 없는 요청이에요, 개발팀에 문의해주세요, 문의코드 : TSAB0001"
                logger.error(f"[TSAB0001] - {action}")
                self.slack_manager.post_ephemeral_message(
                    user=self.user.slack_user_id, text=msg, thread_ts=thread_ts
                )
                continue

            match type:
                case "button":
                    self.button(action, thread_ts)
                case "static_select":
                    self.static_select(action, thread_ts)
                case _:
                    print("정의되지 않는 기능")

    def button(self, action: dict, thread_ts: str):
        """
        action = {
            "action_id": "사용자정의",
            "type": "button",
            "block_id": "Edsvd",
            "text": {"type": "plain_text", "text": "Next 5 Results", "emoji": True},
            "value": "click_me_123",
            "action_ts": "1727962974.218652",
        }
        """
        action_id = action.get("action_id")

        match action_id:
            case "download":
                self.__action_download(action, thread_ts)
            case _:
                pass

    def static_select(self, action: dict, thread_ts: str):
        """
        action = {
            "action_id": "사용자정의",
            "type": "static_select",
            "block_id": "UH84N",
            "selected_option": {
                "text": {"type": "plain_text", "text": "Read it", "emoji": True},
                "value": "value-1",
            },
            "placeholder": {"type": "plain_text", "text": "Manage", "emoji": True},
            "action_ts": "1727962940.466486",
        }
        """
        ...

    def __action_download(self, action, thread_ts):
        value = action.get("value")
        if value == "Approve":
            self.slack_manager.text_msg("승인", thread_ts)
        elif value == "Deny":
            self.slack_manager.text_msg("거절", thread_ts)
