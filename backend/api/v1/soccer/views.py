from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication

from api.v1.soccer.models import Soccer
from api.v1.soccer.serializer import SoccerListSerializer, SoccerSerializer

from datetime import datetime


class SoccerLevelView(APIView):
    def get(self, request):
        return Response(Soccer.Level.choices, status=200)


class SoccerView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    # authentication_classes = BasicAuthentication

    queryset = Soccer.objects.all()
    serializer_class = SoccerSerializer

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def get_serializer_class(self):
        if self.request.method == "GET":
            if "pk" not in self.kwargs:
                return SoccerListSerializer
        return self.serializer_class

    def list(self, request):
        if not ("view" in request.GET and "month" in request.GET):
            return Response({"message": "parameter_error"}, status=400)

        view = request.GET.get("view")
        if view not in ("main", "list"):
            return Response({"message": "view는 main/list만 가능합니다"}, status=400)

        month = request.GET.get("month")
        try:
            month = datetime.strptime(month, "%Y-%m")  # yyyy-mm 형식으로 변환 시도
        except ValueError:  # 변환 실패 시 예외 발생
            return Response({"message": "yyyy-mm 형식"}, status=400)

        soccer = (
            self.get_queryset()
            .select_related("where")
            .filter(when__startswith=request.GET.get("month"))
        )
        serializer = self.get_serializer_class()
        soccer = serializer(instance=soccer, many=True)
        return Response(soccer.data, status=200)

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
