from django.shortcuts import render
from config.settings import logger_info

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


def index(request):
    logger_info.info("INFO 레벨로 출력")
    return render(request, "chat/index.html", {})


def room(request, room_name):
    logger_info.info("INFO 레벨로 출력222")
    return render(request, "chat/room.html", {"room_name": room_name})


def roomWithUser(request, room_name, user_name):
    return render(
        request,
        "chat/roomWithUser.html",
        {"room_name": room_name, "user_name": user_name},
    )
