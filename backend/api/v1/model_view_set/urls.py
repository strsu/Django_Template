from rest_framework import routers
from django.urls import path

from api.v1.model_view_set import views


router = routers.SimpleRouter(trailing_slash=True)
router.register(r"", views.ProductView)

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
] + router.urls
