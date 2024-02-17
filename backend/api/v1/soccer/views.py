from rest_framework import generics, mixins, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication

from rest_framework.pagination import PageNumberPagination  # 👈 페이지 기반 파지네이션

from api.v1.soccer.models import Soccer, SoccerPlace
from api.v1.soccer.serializer import (
    SoccerListSerializer,
    SoccerSerializer,
    SoccerPlaceSerializer,
)

from config.exceptions.custom_exceptions import CustomException
from api.common.message import UserFault

from datetime import datetime


class SoccerLevelView(APIView):
    def get(self, request):
        return Response(Soccer.Level.choices, status=200)


class SoccerPlaceView(
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    queryset = SoccerPlace.objects.all()
    serializer_class = SoccerPlaceSerializer

    def put(self, request, pk):
        return self.update(request, pk)


# StudentPagination # 👈 개별 View에 적용시킬 Pagination Class
class SoccerPagination(PageNumberPagination):  # 👈 PageNumberPagination 상속
    page_size = 3


class SoccerView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Soccer.actives.all()
    serializer_class = SoccerSerializer
    pagination_class = SoccerPagination  # 👈 pagination_class 값에 매핑

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
        if self.request.method == "GET":
            if "pk" not in self.kwargs:
                return SoccerListSerializer
        return self.serializer_class

    def get_pagination_class(self):
        return self.pagination_class

    def list(self, request):
        if not ("view" in request.GET and "month" in request.GET):
            raise CustomException(UserFault.NOT_FOUND)

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

    def post(self, request, *args, **kwargs):
        # 직접 serializer를 사용하는 경우
        # soccer_serializer = SoccerSerializer(
        #     data=request.data, context={"request": request}
        # )
        # soccer_serializer.is_valid(raise_exception=True)
        # soccer = soccer_serializer.save()
        # soccer.save()
        return super().create(request, *args, **kwargs)

    def patch(self, request, pk):
        return self.update(request, pk)

    def perform_destroy(self, instance):
        instance.delete()
        instance.save()

    def delete(self, request, pk):
        return self.destroy(request, pk)
