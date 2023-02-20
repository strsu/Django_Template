from django.shortcuts import render
import logging

logger = logging.getLogger("logstash")


def index(request):
    logger.info("INFO 레벨로 출력")
    print("asdfasdf")
    return render(request, "chat/index.html", {})


def room(request, room_name):
    user_name = request.GET.get("userName")
    logger.info("INFO 레벨로 출력222")
    return render(
        request, "chat/room.html", {"room_name": room_name, "user_name": user_name}
    )
