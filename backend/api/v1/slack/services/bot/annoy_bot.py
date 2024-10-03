from .bot import Bot
from api.v1.slack.services.slack_manager import SlackManager


class AnnoyBot(Bot):

    TOKEN = ""
    BOT_TOKEN = ""

    def __init__(self, channel, user):
        """
        user = {'id': 'U05354JBYNR', 'username': 'jolie0215', 'name': 'jolie0215', 'team_id': 'T05382YA2QJ'}
        """
        self.slack_manager = SlackManager(channel, self.BOT_TOKEN)
        self.user = user

    def actions(self, actions, thread_ts):
        for action in actions:

            type = action.get("type")

            match type:
                case "button":
                    self.button(action, thread_ts)
                case "static_select":
                    self.static_select(action, thread_ts)
                case _:
                    print("정의되지 않는 기능")

    def button(self, action, thread_ts):
        """
        action = {
            "action_id": "gsGb7",
            "block_id": "Edsvd",
            "text": {"type": "plain_text", "text": "Next 5 Results", "emoji": True},
            "value": "click_me_123",
            "type": "button",
            "action_ts": "1727962974.218652",
        }
        """
        value = action.get("value")

        if value == "True":
            self.slack_manager.text_msg("승인", thread_ts)
        elif value == "False":
            self.slack_manager.text_msg("거절", thread_ts)
        else:
            self.slack_manager.text_msg(f"알 수 없는 명령: {value}", thread_ts)

    def static_select(self, action, thread_ts):
        """
        action = {
            "type": "static_select",
            "action_id": "NkJV9",
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
