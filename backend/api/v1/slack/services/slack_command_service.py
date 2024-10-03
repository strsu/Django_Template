from .command.command_celery import CommandCelery


class SlackCommandService:

    def __init__(self): ...

    @classmethod
    def find_command(cls, app_id, token, command):
        match app_id:
            case "A07Q5H96LF4":
                if CommandCelery.TOKEN == token and command == "/celery":
                    return CommandCelery

        return None
