from django.db import models, connection

from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point, Polygon, MultiPolygon
from django.contrib.gis.measure import Distance

from api.common.models import TimestampModel


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
        self.coord = Point((float(self.longitude), float(self.latitude)), srid=4326)
        super().save(*args, kwargs)

    @classmethod
    def get_places(cls, longitude, latitude, radius, map_type):

        queryset = Map.objects.filter(map_type=map_type)
        queryset = queryset.filter(
            coord__distance_lt=(
                Point(float(longitude), float(latitude)),
                Distance(m=float(radius)),
            )
        )

        return queryset

    class Meta:
        verbose_name = "장소"
        verbose_name_plural = "장소"


class ClothingCollectionBox(TimestampModel):
    update_at = models.DateField("공공데이터 업데이트 날짜", null=True, blank=True)

    class Meta:
        verbose_name = "헌옷수거함"
        verbose_name_plural = "헌옷수거함"


class PolyMap(models.Model):
    name = models.CharField(max_length=255)
    eng_name = models.CharField(max_length=255)
    location = gis_models.MultiPolygonField(srid=4326, spatial_index=True)

    @classmethod
    def save_polymap(cls, name: str, eng_name: str, coordinates: list):
        poly_list = []
        for coor in coordinates:
            poly_list.append(Polygon(coor))

        return PolyMap.objects.create(
            name=name, eng_name=eng_name, location=MultiPolygon(poly_list)
        )

    @classmethod
    def convert_shp2json(cls, input_path, output_path):
        """
        dbf, shp, shx 파일이 한 폴더에 있어야 한다.
        """
        import geopandas as gpd

        df = gpd.read_file(input_path, encoding="CP949")
        df = df.set_crs(
            epsg=5179
        )  # EPSG 5179는 한국에서 주로 사용되는 좌표계 중 하나로, 흔히 'Korea 2000 / Unified CS'
        df = df.to_crs(
            epsg=4326
        )  # EPSG 4326은 WGS 84 좌표계로, 위도와 경도로 표현되는 글로벌 표준 좌표계
        df.to_file(driver="GeoJSON", filename=output_path)

    class Meta:
        verbose_name = "폴리곤맵"
        verbose_name_plural = "폴리곤맵"
