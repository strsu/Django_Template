from django.db import transaction
from django.core.cache import cache
from django.utils import timezone

from api.common.utils import kst_to_unixtime, unixtime_to_kst, now_unixtime

from .action_interface import ActionInterface

from api.v1.slack.models import SlackInteractivityHistory

from datetime import timedelta


class ElectronAction(ActionInterface):
    """
    전기사용량을 가져올 때, 전기를 특정용량 이상 사용하고 있는 경우 운영팀에 이슈를 알리고,
    액션 타입에 따라 해결하는 기능
    """

    ACTION_PREFIX = "electron"

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

    def resolve(self, action: dict, state: dict, thread_ts: str):
        """
        전파된 이슈를 action 종료에 따라 비즈니스로직을 수행하는 함수
        """

        action_id = action.get("action_id")
        action_ts = action.get("action_ts")

        """
        action prefix는 모두 동일하게 시작해도, 최종 행동 결정 action_id가 아니라면 로직을 수행할 필요가 없다.
        """
        if action_id not in [
            f"{self.ACTION_PREFIX}__approve",
            f"{self.ACTION_PREFIX}__deny",
        ]:
            return False

        cache_key = f"{self.ACTION_PREFIX}_{thread_ts}"

        if cache.set(
            cache_key, "1", nx=True, timeout=5
        ):  # 5초 동안 잠금 유지, 실수로 캐시가 안 지워져도 5초 뒤에는 지워질 수 있도록!
            with transaction.atomic():
                try:
                    sih = SlackInteractivityHistory.objects.get(
                        alerted_at=thread_ts, action_prefix=self.ACTION_PREFIX
                    )
                except SlackInteractivityHistory.DoesNotExist:
                    sih = SlackInteractivityHistory(
                        executor=self.user,
                        alerted_at=thread_ts,
                        action_prefix=self.ACTION_PREFIX,
                        executed_at=action_ts,
                    )
                else:

                    executed_dt = unixtime_to_kst(float(sih.executed_at)).strftime(
                        "%Y-%m-%d %H:%M"
                    )

                    self.slack_manager.post_ephemeral_message(
                        user=self.user.slack_user_id,
                        text=f"이 작업은 {sih.executor.user.username}에 의해서 {executed_dt}에 이미 수행되었어요\n수행결과: {sih.execute_result}",
                        thread_ts=thread_ts,
                    )
                    return False

                alert_dt = unixtime_to_kst(float(thread_ts))
                action_dt = unixtime_to_kst(float(action_ts))

                if action_dt > alert_dt + timedelta(minutes=10):
                    self.slack_manager.post_ephemeral_message(
                        user=self.user.slack_user_id,
                        text="너무 오래된 알림이라 지금은 수행할 수 없어요",
                        thread_ts=thread_ts,
                    )
                    return False

                action_type = action.get("type")
                data = self.extract(state)

                match action_type:
                    case "button":
                        result = self.button(action, data, thread_ts)
                        sih.execute_result = result
                        sih.save()

        else:
            self.slack_manager.post_ephemeral_message(
                user=self.user.slack_user_id,
                text="작업을 수행중이에요, 잠시만 기다려주세요!",
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
