from django.shortcuts import render, redirect
import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny


from .models import Group, Message


class ChatApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, "chat/index.html", {})


class ChatPlayApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return redirect(f"/api/chat/")

    def post(self, request):
        room_name = request.data.get("room_name")
        user_name = request.data.get("user_name")
        return render(
            request,
            "chat/roomWithUser.html",
            {"room_name": room_name, "user_name": user_name},
        )


class ChatPlayLogApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        name = request.GET.get("name")
        name = "mzoffice"
        group = Group.objects.get(name=name)

        message = Message.objects.filter(group=group).order_by("timestamp")

        message_list = []

        for msg in message:
            message_list.append(
                {
                    "msg": {
                        "flag": False,
                        "message": msg.content,
                        "name": msg.name,
                        "time": msg.timestamp,
                    }
                }
            )

        return Response({"history": message_list}, status=200)


def index(request):
    # 여기서 request는 WSGIRequest 이다
    # 근데 위 drf의 request와 다른 객체이다!!!
    # 이건 장고 자체 rest 인 듯..!
    return render(request, "chat/index.html", {})
