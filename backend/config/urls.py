"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Django Template API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r"^admin_tools/", include("admin_tools.urls")),
    path("admin/", admin.site.urls),
    re_path(
        r"^api/swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^api/swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^api/redoc/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path("api/chat/", include("api.v1.chat.urls")),
    re_path("api/v1/file/", include("api.v1.file.urls")),
    re_path("api/v1/blog/", include("api.v1.blog.urls")),
    re_path("api/v1/user/", include("api.v1.user.urls")),
    re_path("api/v1/soccer/", include("api.v1.soccer.urls")),
    re_path("api/v1/movie/", include("api.v1.rating.urls")),
    re_path("api/v1/celery/", include("api.v1.celery_practice.urls")),
    re_path("api/v1/modelViewSet/", include("api.v1.model_view_set.urls")),
    re_path(
        "api/v1/serializerWithoutModel/",
        include("api.v1.serializer_without_model.urls"),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
