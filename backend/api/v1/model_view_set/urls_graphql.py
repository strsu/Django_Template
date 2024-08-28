from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView
from rest_framework import routers

from .schema import product_type_schema

"""
schema를 settings.py에서 줘도 되지만, 그냥 이렇게 url에서 주는게 더 깔끔할 것 같다!!
"""

urlpatterns = [
    path(
        "product/",
        csrf_exempt(GraphQLView.as_view(graphiql=True, schema=product_type_schema)),
    ),
]
