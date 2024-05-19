from django.urls import path, re_path
from api.v1.file import views

"""
    re_path: 정규식을 적용한 path
"""

urlpatterns = [
    path("", views.FileView.as_view(), name=""),
    path("media/", views.VideoListView.as_view(), name=""),
    path("pdf/merge/", views.PDFMergeView.as_view(), name="pdf"),
    path("pdf/upload/", views.PDFUploadView.as_view(), name=""),
    path("pdf/upload2/", views.PDFUpload2View.as_view(), name=""),
]
