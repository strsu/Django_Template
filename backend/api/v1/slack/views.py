from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.shortcuts import render
from django.contrib.auth import authenticate

from api.common import cache

from .services.slack_interactivity_service import SlackInteractivityService
from .services.slack_command_service import SlackCommandService
from .services.slack_verify_service import SlackVerifyService

import json


class SlackInteractiveView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        payload = request.data.get("payload")
        payload = json.loads(payload)

        for key, value in payload.items():
            print(key, value)

        user = payload.get("user")
        app_id = payload.get("api_app_id")
        token = payload.get("token")
        type = payload.get("type")

        actions = payload.get("actions")  # 현재 선택한 액션
        callback_id = payload.get("view", {}).get("callback_id")

        channel = None
        data = {}

        if type == "block_actions":
            channel = payload.get("channel").get("id")
        elif type == "view_submission":
            data = cache.getKey(callback_id)
            if data:
                channel = data.get("channel")
            else:
                return Response(status=500)

        slack_auth = SlackVerifyService.verify_user(user.get("id"), channel, actions)

        if slack_auth:
            BOT = SlackInteractivityService.find_app(app_id, token)
            if BOT:
                bot = BOT(channel, slack_auth)
                if type == "block_actions":
                    bot.actions(actions, payload)
                elif type == "view_submission":
                    bot.view(payload, data)

        return Response(status=200)


class SlackCommandView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        slack = request.data

        token = slack.get("token")
        app_id = slack.get("api_app_id")

        user = {"id": slack.get("user_id"), "name": slack.get("user_name")}

        command_type = slack.get("command")
        command_text = slack.get("text")

        channel = {
            "id": slack["channel_id"],  # slack.get("channel_id")을 쓰면 None을 리턴함,,
            "name": slack.get("channel_name"),
        }

        App = SlackCommandService.find_command(app_id, token, command_type)

        if App:
            bot = App(channel, user)
            bot.execute(command_text)

        return Response(status=200)


class SlackUserVerifyView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        token = request.GET.get("token")
        slack = request.GET.get("slack")

        if not cache.getKey(f"slack_{slack}"):
            return render(request, "invalid.html")
        return render(request, "verify.html", {"token": token, "slack": slack})

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        token = request.POST.get("token")
        slack_user_id = request.POST.get("slack")

        # 사용자 인증
        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response({"error": "사용자 인증 실패"}, status=401)

        is_validate, msg = SlackVerifyService.verify_validate(user, slack_user_id, token)

        if is_validate:
            return Response({"message": msg}, status=200)

        return Response({"error": msg}, status=400)
