from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Map


class ClothingCollectingBoxView(APIView):
    def get(self, request):
        longitude = request.GET.get("longitude")
        latitude = request.GET.get("latitude")
        radius = request.GET.get("radius", 1000)

        queryset = Map.get_places(longitude, latitude, radius, Map.MapType.cloth)

        result = []
        for q in queryset:
            result.append([q.road_address, q.latitude, q.longitude])

        return Response(result, status=200)
