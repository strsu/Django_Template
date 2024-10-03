from .bot.annoy_bot import AnnoyBot


class SlackInteractivityService:

    def __init__(self): ...

    @classmethod
    def find_app(cls, app_id, token):
        match app_id:
            case "A07Q5H96LF4":
                if AnnoyBot.TOKEN == token:
                    return AnnoyBot

        return None
