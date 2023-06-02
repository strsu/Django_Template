from django.urls import path
from api.v1.rating import views

"""
    re_path: 정규식을 적용한 path
"""

urlpatterns = [
    path("view/", views.MovieApiView.as_view(), name=""),
    path("", views.MovieView.as_view(), name=""),
    path("<int:pk>/", views.MovieView.as_view(), name=""),
    path("genre/", views.GenreView.as_view(), name=""),
    path("<int:pk>/genre/", views.MovieGenreView.as_view(), name=""),
    path("<int:pk>/nation/", views.MovieNationView.as_view(), name=""),
    path("<int:pk>/rating/", views.MovieRatingView.as_view(), name=""),
    path("rate/type/", views.MovieRateTypeView.as_view(), name=""),
    path("nation/", views.NationView.as_view(), name=""),
]
