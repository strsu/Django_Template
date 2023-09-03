from rest_framework import viewsets
from rest_framework.response import Response

from api.v1.model_view_set.models import Product, ProductType
from api.v1.model_view_set.serializer import (
    ProductSerializer,
    ProductRawSerializer,
    ProductTypeSerializer,
)


class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    lookup_field = "pk"

    def get_serializer_class(self):
        print(self.kwargs)
        return self.serializer_class

    def get_queryset(self):
        return super().get_queryset().filter()

    def get_object(self):
        return super().get_object()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        print("create 이후 작업 정의")
        return response

    def update(self, request, *args, **kwargs):
        # *args, **kwargs <- 필수, pk 때문인듯?
        response = super().update(request, *args, **kwargs)
        print("update 이후 작업 정의")
        return response

    def partial_update(self, request, *args, **kwargs):
        # *args, **kwargs <- 필수, pk 때문인듯?
        response = super().partial_update(request, *args, **kwargs)
        print("partial_update 이후 작업 정의")
        return response

    def destroy(self, request, *args, **kwargs):
        # *args, **kwargs <- 필수, pk 때문인듯?
        response = super().destroy(request, *args, **kwargs)
        print("destroy 이후 작업 정의")
        return response


class ProductTypeView(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    http_method_names = ["post"]  # 이렇게 하면 simplerouter에서 post만 연결해준다.


class ProductRawView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductRawSerializer
