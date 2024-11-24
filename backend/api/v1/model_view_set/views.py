from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from django.core.serializers import serialize
from django.forms.models import model_to_dict
from django.db.models import Prefetch, Q

from api.v1.model_view_set.models import (
    Product,
    ProductType,
    ProductOrder,
    ProductTag,
    ProductOrderShipping,
)
from api.v1.model_view_set.serializer import (
    ProductSerializer,
    ProductDetailSerializer,
    ProductUploadSerializer,
    ProductRawSerializer,
    ProductTypeSerializer,
)


class ProductView(viewsets.ModelViewSet):
    """
    (1) Product.objects.select_related("type").prefetch_related(
        "productorder_set"
    )
        1. purchaser를 미리 가져올 수 없다
        2. product_order에 조건을 걸 수 없다

    (2) Product.objects.select_related("type").filter(
        Q(productorder__id__isnull=False) | Q(productorder__id__isnull=True)
    )
        1. Q를 써야 모든 product를 가져올 수 있다
        2. (1)에 비해 쿼리가 많다

    """

    queryset = Product.objects.select_related("type")
    serializer_class = ProductSerializer

    lookup_field = "pk"

    def get_serializer_class(self):
        if self.request.method == "GET":
            if self.action == "list":
                return ProductSerializer
            elif self.action == "retrieve":
                return ProductDetailSerializer
        return ProductUploadSerializer

    def get_queryset(self):
        if self.request.method == "GET":
            if self.action == "retrieve":
                return self.queryset.prefetch_related(
                    Prefetch(
                        "productorder_set",
                        queryset=ProductOrder.objects.select_related("purchaser")
                        .all()
                        .prefetch_related(
                            Prefetch(
                                "shipping", queryset=ProductOrderShipping.objects.all()
                            )
                        ),
                    )
                )
        return super().get_queryset()

    def get_object(self):
        return super().get_object()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        print("list 이후 작업 정의")
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        print("retrieve 이후 작업 정의")
        return response

    @extend_schema(
        request=ProductSerializer,
        responses={201: ProductSerializer},
    )
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


class ProductTagView(APIView):

    def get(self, request):
        name = request.GET.get("name")
        tag = ProductTag.get_tag_by_name(name)
        return Response(model_to_dict(tag), status=200)


class ProductRawView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductRawSerializer


class ProductOrderView(APIView):

    def post(self, request, product_id):

        amount = request.data.get("amount")

        if not amount:
            return Response({"message": "구매수량을 입력해주세요."}, status=400)

        user = request.user
        # ProductOrder.purchase(product_id, user, amount)
        ProductOrder.purchase_with_retry_only_isolation(product_id, user, amount)

        return Response(status=200)
