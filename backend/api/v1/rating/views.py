from django.shortcuts import render, redirect
from django.db.models import Avg, Count, Sum
from django.http import HttpResponse

from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination

from config.exceptions.custom_exceptions import CustomException
from api.common.message import UserFault

from api.v1.rating.models import Nation, Genre, Movie, MovieRateType, MovieRating
from api.v1.rating.serializer import (
    NationSerilizer,
    GenreSerilizer,
    MovieSerializer,
    MovieRateTypeSerializer,
    MovieRatingSerializer,
)
from api.v1.rating.forms import FileUploadForm

from api.v1.rating.tasks import transcoding_task

from datetime import datetime


class MoviePagination(PageNumberPagination):  # 👈 PageNumberPagination 상속
    page_size = 100


class MovieApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, "video/index.html", {})


class MovieUploadApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        fileuploadForm = FileUploadForm
        context = {
            "form": fileuploadForm,
        }

        return render(request, "video/upload.html", context)

    def post(self, request):
        """
        이 form으로 파일을 업로드 하는 것의 문제점은 파일을 메모리에 저장을 하기 때문에
        메모리가 꽉 차면 저장에 실패하는 문제가 발생한다.
        """
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            filename = instance.file.name.split("/")[-1]
            transcoding_task.delay(filename)

        return HttpResponse("success")


class GenreView(
    mixins.ListModelMixin,
    generics.GenericAPIView,
):
    permission_classes = [AllowAny]

    queryset = Genre.objects.all().order_by("content", "genre")
    serializer_class = GenreSerilizer
    pagination_class = MoviePagination

    def get(self, request, *args, **kwargs):
        return self.list(request)


class NationView(
    mixins.ListModelMixin,
    generics.GenericAPIView,
):
    permission_classes = [AllowAny]

    queryset = Nation.objects.all()
    serializer_class = NationSerilizer
    pagination_class = MoviePagination

    def get(self, request, *args, **kwargs):
        return self.list(request)


class MovieRateTypeView(
    mixins.ListModelMixin,
    generics.GenericAPIView,
):
    permission_classes = [AllowAny]

    queryset = MovieRateType.objects.all()
    serializer_class = MovieRateTypeSerializer
    pagination_class = MoviePagination

    def get(self, request, *args, **kwargs):
        return self.list(request)


class MovieView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    permission_classes = [AllowAny]

    queryset = Movie.actives.all()
    serializer_class = MovieSerializer
    pagination_class = MoviePagination

    def get_queryset(self):
        return self.queryset.filter(deleted_at__isnull=True, file__contains="media")

    def get_serializer_class(self):
        return self.serializer_class

    def get(self, request, *args, **kwargs):
        if "pk" in kwargs:
            return self.retrieve(request, kwargs["pk"])
        else:
            data = self.list(request)
            id_list = [d["id"] for d in data.data["results"]]

            nation = Nation.objects.get(nation="한국")
            nation_obj = nation.movie_nation.all()  # 한국 영화를 모두 가져온다.

            for m in nation_obj:
                print(m.__dict__)

            movie_rating = (
                MovieRating.objects.filter(movie_id__in=id_list)
                .values("movie")
                .annotate(avg_score=(Sum("score") / Count("score")))
            )

            movie_rating_dict = {}

            for obj in movie_rating:
                movie_rating_dict[obj["movie"]] = round(obj["avg_score"], 2)

            for i, d in enumerate(data.data["results"]):
                if d["id"] in movie_rating_dict:
                    data.data["results"][i]["avg_score"] = movie_rating_dict[d["id"]]
                else:
                    data.data["results"][i]["avg_score"] = 0

            return data

    def post(self, request):
        try:
            obj = self.queryset.get(
                title=request.data.get("title"), folder=request.data.get("folder")
            )
        except:
            # 없으면 생성
            return self.create(request)
        else:
            serializer = self.get_serializer_class()
            movie = serializer(instance=obj)
            return Response(movie.data, status=200)

    def patch(self, request, pk):
        return self.update(request, pk)

    def perform_destroy(self, instance):
        instance.delete()
        instance.save()

    def delete(self, request, pk):
        return self.destroy(request, pk)


class MovieGenreView(
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    permission_classes = [AllowAny]

    queryset = Genre.objects.all()
    serializer_class = GenreSerilizer

    def get_queryset(self):
        return super().get_queryset().filter()

    def get_serializer_class(self):
        return self.serializer_class

    def post(self, request, pk):
        movie = Movie.actives.get(id=pk)
        genre = Genre.objects.get(id=request.data.get("genre"))
        if genre in movie.genre.all():
            movie.genre.remove(genre)
        else:
            movie.genre.add(genre)
        return Response(status=200)


class MovieNationView(
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    permission_classes = [AllowAny]

    queryset = Nation.objects.all()
    serializer_class = NationSerilizer

    def get_queryset(self):
        return super().get_queryset().filter()

    def get_serializer_class(self):
        return self.serializer_class

    def post(self, request, pk):
        movie = Movie.actives.get(id=pk)
        nation = Nation.objects.get(id=request.data.get("nation"))
        movie.nation = nation
        movie.save()
        return Response(status=200)


class MovieRatingView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    permission_classes = [AllowAny]

    queryset = MovieRating.objects.all()
    serializer_class = MovieRatingSerializer
    pagination_class = MoviePagination

    def get_queryset(self):
        return self.queryset.filter(movie_id=self.kwargs["pk"])
        return super().get_queryset().filter()

    def get_serializer_context(self):
        return {"pk": self.kwargs["pk"]}

    def get_serializer_class(self):
        return self.serializer_class

    def get(self, request, pk):
        return self.list(request, pk)

    def post(self, request, pk):
        movie = Movie.actives.get(id=pk)
        rate_type = MovieRateType.objects.get(id=request.data.get("rate_type"))
        movie_rating, created = MovieRating.objects.update_or_create(
            movie=movie,
            rate_type=rate_type,
            defaults={"score": float(request.data.get("score"))},
        )
        movie_rating.save()
        return Response(status=200)
