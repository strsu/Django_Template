from api.v1.slack.services.slack_manager import SlackManager


class CommandCelery:
    TOKEN = ""
    BOT_TOKEN = ""

    def __init__(self, channel, user):
        self.channel = channel
        self.user = user

        self.slack_manager = SlackManager(channel.get("id"), self.BOT_TOKEN)

    def execute(self, command):
        command = command.lower()

        if self.channel["name"] == "directmessage":
            return self.slack_manager.text_msg("개인 DM에서 사용할 수 없습니다.")

        match command:
            case "help":
                help = [
                    {
                        "type": "rich_text",
                        "elements": [
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {
                                        "type": "text",
                                        "text": "명령어 모음은 다음과 같습니다.\n",
                                    }
                                ],
                            },
                            {
                                "type": "rich_text_list",
                                "style": "bullet",
                                "indent": 0,
                                "border": 0,
                                "elements": [
                                    {
                                        "type": "rich_text_section",
                                        "elements": [
                                            {
                                                "type": "text",
                                                "text": "A기능",
                                                "style": {"bold": True},
                                            },
                                            {
                                                "type": "text",
                                                "text": " : A기능에 대한 설명",
                                            },
                                        ],
                                    },
                                    {
                                        "type": "rich_text_section",
                                        "elements": [
                                            {
                                                "type": "text",
                                                "text": "B기능",
                                                "style": {"bold": True},
                                            },
                                            {
                                                "type": "text",
                                                "text": " : B기능에 대한 설명",
                                            },
                                        ],
                                    },
                                ],
                            },
                        ],
                    }
                ]
                return self.slack_manager.block_msg(help)
            case _:
                return None
