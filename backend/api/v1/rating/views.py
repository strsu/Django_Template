from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication

from config.exceptions.custom_exceptions import CustomException
from api.common.message import UserFault

from api.v1.rating.models import Movie
from api.v1.rating.serializer import MovieSerializer

from datetime import datetime
import ffmpeg


class MovieView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_queryset(self):
        """
        여기서 공통으로 사용하는 queryset에 작업을 하는 방향이 좋은 것 같다.
            -> 어차피 Mixin에서 get_queryset을 호출해서 query를 사용하기 때문에!
        아래 filter에 user를 넣었기 때문에 자동으로 user가 걸러진다!
        """
        return (
            super()
            .get_queryset()
            .filter(deleted_at__isnull=True, user=self.request.user)
        )

    def get_serializer_class(self):
        return self.serializer_class

    def get(self, request, *args, **kwargs):
        if "pk" in kwargs:
            return self.retrieve(request, kwargs["pk"])
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def patch(self, request, pk):
        return self.update(request, pk)

    def perform_destroy(self, instance):
        instance.delete()
        instance.save()

    def delete(self, request, pk):
        return self.destroy(request, pk)
