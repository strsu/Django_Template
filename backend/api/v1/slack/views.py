from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .services.slack_interactivity_service import SlackInteractivityService
from .services.slack_command_service import SlackCommandService

import json


class SlackInteractiveView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        slack = request.data.get("payload")

        slack = json.loads(slack)

        user = slack.get("user")
        app_id = slack.get("api_app_id")
        token = slack.get("token")
        channel = slack.get("channel").get("id")
        thread_ts = slack.get("container").get("message_ts")
        actions = slack.get("actions")

        App = SlackInteractivityService.find_app(app_id, token)

        if App:
            bot = App(channel, user)
            bot.actions(actions, thread_ts)

        for key, value in slack.items():
            print(key, value)

        return Response(status=201)


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
