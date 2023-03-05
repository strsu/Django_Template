from django.shortcuts import render
from config.settings import logger

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


@permission_classes([IsAuthenticated])
def index(request):
    logger.info("INFO 레벨로 출력")
    return render(request, "chat/index.html", {})


@permission_classes([IsAuthenticated])
def room(request, room_name):
    user_name = request.GET.get("userName")
    logger.info("INFO 레벨로 출력222")
    return render(
        request, "chat/room.html", {"room_name": room_name, "user_name": user_name}
    )
