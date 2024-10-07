from .command.command_celery import CommandCelery


class SlackCommandService:

    def __init__(self): ...

    @classmethod
    def find_command(cls, app_id, token, command):
        match app_id:
            case CommandCelery.APP_ID:
                if CommandCelery.TOKEN == token and command == CommandCelery.COMMAND:
                    return CommandCelery

        return None
