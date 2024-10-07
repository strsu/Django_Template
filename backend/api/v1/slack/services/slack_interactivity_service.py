from .interativity.annoy_app import AnnoyApp


class SlackInteractivityService:

    def __init__(self): ...

    @classmethod
    def find_app(cls, app_id, token):
        match app_id:
            case AnnoyApp.APP_ID:
                if AnnoyApp.TOKEN == token:
                    return AnnoyApp

        return None
