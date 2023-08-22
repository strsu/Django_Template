from django.urls import path
from api.v1.model_view_set import views

product_list = views.ProductView.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

product_detail = views.ProductView.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

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
    path("", product_list, name=""),
    path("<int:pk>", product_detail, name=""),
    path("raw", product_raw_list, name=""),
    path("raw/<int:pk>", product_raw_detail, name=""),
]
