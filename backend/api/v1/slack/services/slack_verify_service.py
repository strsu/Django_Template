from api.v1.slack.models import SlackAuth
from api.v1.slack.services.slack_manager import SlackManager


class SlackVerifyService:

    BOT_TOKEN = ""

    @classmethod
    def verify_user(cls, user_id, channel_id, actions=[]):
        slack_auth, created = SlackAuth.actives.get_or_create(slack_user_id=user_id)

        # 인증된 회원인 경우
        if slack_auth.user:
            return slack_auth

        is_validate = cls.__check_validate__(actions)

        msg = "풍부한 기능제공을 위해서는 사용자 인증이 필요해요"
        if is_validate:
            if slack_auth.exist_token():
                return None
            else:
                msg = "인증기한이 만료되었어요, 10분이내 인증을 완료해주세요!"

        token = slack_auth.generate_auth_token()

        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": msg,
                },
                "accessory": {
                    "action_id": "authorization",
                    "type": "button",
                    "text": {"type": "plain_text", "text": "인증하기", "emoji": True},
                    "value": "verify",
                    "url": f"https://8d9a-59-10-5-91.ngrok-free.app/api/v1/slack/verify/?token={token}&slack={user_id}",
                },
            }
        ]

        slack_manager = SlackManager(channel_id, cls.BOT_TOKEN)
        slack_manager.post_ephemeral_message(user=user_id, blocks=blocks)

        return None

    @classmethod
    def verify_validate(cls, user, slack_user_id, token):
        try:
            slack_auth = SlackAuth.actives.get(slack_user_id=slack_user_id)
        except SlackAuth.DoesNotExist:
            return False, "유효하지 않은 접근이에요"

        if slack_auth.user is not None:
            return (
                True,
                "인증이 완료된 사용자에요, 지속적으로 인증요구가 발생하면 개발팀에 문의해주세요",
            )

        if not slack_auth.exist_token():
            return False, "인증 만료 기간을 넘었어요"

        if slack_auth.verify_token(token):
            slack_auth.user = user
            slack_auth.save()
            return True, f"{user.username}님 안녕하세요, 인증을 성공적으로 맞췄어요"

        return False, "인증 토큰이 유효하지 않아요"

    @classmethod
    def __check_validate__(self, actions):
        is_auth_action = False
        for action in actions:
            if (
                action.get("type") == "button"
                and action.get("action_id") == "authorization"
                and action.get("value") == "verify"
            ):
                is_auth_action = True
                break

        return is_auth_action
