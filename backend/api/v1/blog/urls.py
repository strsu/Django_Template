from django.urls import path, re_path
from api.v1.blog import views

"""
    re_path: 정규식을 적용한 path
"""

urlpatterns = [
    path("", views.BlogApiView.as_view(), name=""),
    path("list/", views.BlogListMixins.as_view(), name=""),
    path("detail/<int:pk>/", views.BlogDetailMixins.as_view(), name=""),
]
