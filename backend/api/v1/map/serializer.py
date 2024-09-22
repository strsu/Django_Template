from rest_framework import serializers
from rest_framework_gis.fields import GeometryField

from .models import Map


class MapSerilizer(serializers.ModelSerializer):
    coord = GeometryField(help_text="거래장소", required=True)

    class Meta:
        model = Map
