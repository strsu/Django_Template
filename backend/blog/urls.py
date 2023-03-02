from django.urls import re_path
from blog import views

urlpatterns = [
    re_path("", views.BlogList.as_view(), name=""),
    # re_path(r"^blog/$", views.BlogList.as_view(), name=""),
]
