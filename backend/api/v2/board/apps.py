from django.apps import AppConfig


class BoardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.v2.board"
    label = "board_v2"  # v1의 board와 겹치면 안되서 이 선언이 필요하다
