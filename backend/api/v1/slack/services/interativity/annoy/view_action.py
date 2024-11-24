from django.db import transaction
from django.core.cache import cache
from django.utils import timezone

from api.common.utils import kst_to_unixtime, unixtime_to_kst, now_unixtime

from .action_interface import ActionInterface

from api.v1.slack.models import SlackInteractivityHistory

from datetime import timedelta


class ViewAction(ActionInterface):
    """
    전기사용량을 가져올 때, 전기를 특정용량 이상 사용하고 있는 경우 운영팀에 이슈를 알리고,
    액션 타입에 따라 해결하는 기능
    """

    ACTION_PREFIX = "control"

    def __init__(self, user, slack_manager):
        self.user = user
        self.slack_manager = slack_manager

    def alert(self, data):
        """
        slack을 통해 이슈를 전파하는 함수
        """
        blocks = self.binding(data)
        self.slack_manager.block_msg(blocks)

    def binding(self, data):
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "전력을 과하게 사용하고 있어요!",
                    "emoji": True,
                },
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "Section block with radio buttons"},
                "accessory": {
                    "type": "radio_buttons",
                    "action_id": f"{self.ACTION_PREFIX}__radio_buttons",
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "*plain_text option 0*",
                                "emoji": True,
                            },
                            "value": "value-0",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "*plain_text option 1*",
                                "emoji": True,
                            },
                            "value": "value-1",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "*plain_text option 2*",
                                "emoji": True,
                            },
                            "value": "value-2",
                        },
                    ],
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "This is a section block with checkboxes.",
                },
                "accessory": {
                    "type": "checkboxes",
                    "action_id": f"{self.ACTION_PREFIX}__checkboxes",
                    "options": [
                        {
                            "text": {"type": "mrkdwn", "text": "*this is mrkdwn text*"},
                            "description": {
                                "type": "mrkdwn",
                                "text": "*this is mrkdwn text*",
                            },
                            "value": "value-0",
                        },
                        {
                            "text": {"type": "mrkdwn", "text": "*this is mrkdwn text*"},
                            "description": {
                                "type": "mrkdwn",
                                "text": "*this is mrkdwn text*",
                            },
                            "value": "value-1",
                        },
                        {
                            "text": {"type": "mrkdwn", "text": "*this is mrkdwn text*"},
                            "description": {
                                "type": "mrkdwn",
                                "text": "*this is mrkdwn text*",
                            },
                            "value": "value-2",
                        },
                    ],
                },
            },
            {
                "type": "input",
                "element": {
                    "type": "datepicker",
                    "action_id": f"{self.ACTION_PREFIX}__datepicker",
                    "initial_date": timezone.now().strftime("%Y-%m-%d"),
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a date",
                        "emoji": True,
                    },
                },
                "label": {"type": "plain_text", "text": "Label", "emoji": True},
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "action_id": f"{self.ACTION_PREFIX}__approve",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "제어하기",
                        },
                        "style": "primary",
                        "value": "Approve",
                    },
                    {
                        "type": "button",
                        "action_id": f"{self.ACTION_PREFIX}__deny",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "유지하기",
                        },
                        "style": "danger",
                        "value": "Deny",
                    },
                ],
            },
        ]

        return blocks

    def resolve(self, action, payload):
        thread_ts = payload.get("container").get("message_ts")
        message = payload.get("message")  # 보낸 메세지 블록
        blocks = message.get("blocks")

        cache_key = f"{self.ACTION_PREFIX}_{thread_ts}"
        data = cache.get(cache_key)

        if data is None:
            # 처리가능 시간이 지나면 액션버튼 삭제!
            self.delete_action(blocks, thread_ts)

            return False

        trigger_id = payload.get("trigger_id")

        view = {
            "callback_id": trigger_id,
            "title": {"type": "plain_text", "text": "변경입찰", "emoji": True},
            "submit": {"type": "plain_text", "text": "네", "emoji": True},
            "type": "modal",
            "close": {"type": "plain_text", "text": "아니요", "emoji": True},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "정말 취소할까요?",
                        "emoji": True,
                    },
                }
            ],
        }

        result = self.slack_manager.modal_open(trigger_id, view)
        if result:
            if result.get("ok"):
                data["channel"] = self.slack_manager.get_current_channel()
                data["thread_ts"] = thread_ts
                cache.set(trigger_id, data, 600)
        else:
            self.slack_manager.post_ephemeral_message(
                user=self.user.slack_user_id,
                text="요청이 올바르게 수행되지 않았습니다, 다시 눌러주세요",
                thread_ts=thread_ts,
            )

    def extract(self, state):
        pass

    def button(self, action: dict, data: dict, thread_ts: str):
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
        value = action.get("value")
        result_msg = f"알 수 없는 이유로 요청된 작업을 수행할 수 없게 되었어요, 입력된 값: {value}"

        if value == "Approve":
            result_msg = "제안한 요청이 *승인* 되었어요"
        elif value == "Deny":
            result_msg = "제안한 요청이 *거절* 되었어요"

        self.slack_manager.text_msg(result_msg, thread_ts)

        return result_msg

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
