from django.db import models
from django.db import connection

from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point

from api.common.models import TimestampModel


# Create your models here.
class Map(models.Model):

    class MapType(models.IntegerChoices):
        cloth = 1

    map_type = models.IntegerField(
        "지도 데이터 타입", choices=MapType.choices, null=False
    )
    address = gis_models.CharField("지번주소", max_length=256, blank=True, null=False)
    road_address = gis_models.CharField(
        "도로명주소", max_length=256, blank=True, null=False
    )
    latitude = gis_models.FloatField("위도 - 37~", blank=True, null=False)
    longitude = gis_models.FloatField("경도 - 124~", blank=True, null=False)
    coord = gis_models.PointField(
        "좌표",
        srid=4326,
        spatial_index=True,
        null=False,
        default=Point(0, 0, srid=4326),
    )

    def save(self, *args, **kwargs):
        self.coord = Point(self.longitude, self.latitude, srid=4326)
        super().save(*args, kwargs)

    @classmethod
    def get_places(cls, longitude, latitude, map_type):
        def _generate_linestring(longitude, latitude):
            RADIUS = 0.02  # 반경 2km

            left_top = (longitude - RADIUS, latitude + RADIUS)
            right_btm = (longitude + RADIUS, latitude - RADIUS)

            return f"LINESTRING ({left_top[0]} {left_top[1]}, {right_btm[0]} {right_btm[1]})"

        _linestring = _generate_linestring(longitude, latitude)
        _query = f"""
            select id, address, latitude, longitude from map 
            where map_type={map_type} and '{_linestring}'::geometry ~ coord
        """
        queryset = None

        with connection.cursor() as cursor:
            cursor.execute(_query)
            rows = cursor.fetchall()
            queryset = [Map(*row) for row in rows]

        return queryset

    class Meta:
        verbose_name = "map"
        verbose_name_plural = "장소"


class ClothingCollectionBox(TimestampModel):
    update_at = models.DateField("공공데이터 업데이트 날짜", null=True, blank=True)

    class Meta:
        verbose_name = "clothing_collection_box"
        verbose_name_plural = "헌옷수거함"
