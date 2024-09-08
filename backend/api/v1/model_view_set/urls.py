from rest_framework import routers
from django.urls import path

from api.v1.model_view_set import views


router = routers.SimpleRouter(trailing_slash=True)
router.register(r"", views.ProductView)
router.register(r"<int:id>/<str:types>", views.ProductTypeView)

product_type = views.ProductView.as_view({"get": "retrieve"})

product_raw_list = views.ProductRawView.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

product_raw_detail = views.ProductRawView.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

urlpatterns = [
    path("raw/", product_raw_list, name=""),
    path("raw/<int:pk>/", product_raw_detail, name=""),
    path("tag/", views.ProductTagView.as_view(), name=""),
    path("<int:product_id>/order/", views.ProductOrderView.as_view(), name=""),
    # path("<int:pk>/<str:type>/", product_type, name=""),
] + router.urls
