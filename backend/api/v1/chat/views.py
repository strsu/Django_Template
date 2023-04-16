from django.shortcuts import render
from config.settings.base import logger_info
import time

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


def index(request):
    return render(request, "chat/index.html", {})


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})


def roomWithUser(request, room_name, user_name):
    if room_name == "mafia":
        return render(
            request,
            "chat/roomMafia.html",
        )
    else:
        return render(
            request,
            "chat/roomWithUser.html",
            {"room_name": room_name, "user_name": user_name},
        )


def roomRandom(request):
    return render(
        request,
        "chat/roomRandom.html",
        # {"room_name": room_name, "user_name": user_name},
    )
