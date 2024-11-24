from rest_framework import serializers
from rest_framework_gis.fields import GeometryField

from .models import Map


class MapSerilizer(serializers.ModelSerializer):
    """
    "coord": {
        "type": "Point",
        "coordinates":
        [
            12.9721,
            77.5933
        ]
    }
    """

    coord = GeometryField(
        help_text="거래장소",
        required=True,
        error_messages={
            "invalid": "데이터 형식을 올바르게 입력해주세요, Ex : {'type': 'Point', 'coordinates': [위도, 경도]}"
        },
    )

    class Meta:
        model = Map
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(MapSerilizer, self).__init__(*args, **kwargs)
        print(self.fields["coord"].error_messages)

        # you can overide by
        self.fields["coord"].error_messages[
            "invalid"
        ] = "'%s' 값은 True 또는 False 여야 합니다."  # "데이터 형식을 올바르게 입력해주세요, Ex : {'type': 'Point', 'coordinates': [위도, 경도]}"
