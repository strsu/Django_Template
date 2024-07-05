from django.utils import timezone

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.v1.celery.tasks import sleep_task, world


class CeleryPacticeView(APIView):
    def get(self, request):

        world.delay()

        sleep_task.apply_async(
            args=[],
            kwargs={
                "request_at": timezone.now(),
            },
        )

        return Response(status=status.HTTP_200_OK)
