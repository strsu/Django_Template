from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Map
from .serializer import MapSerilizer


class ClothingCollectingBoxView(APIView):
    def get(self, request):
        longitude = request.GET.get("longitude")
        latitude = request.GET.get("latitude")
        radius = request.GET.get("radius", 1000)

        # if longitude is None or latitude is None:
        #     raise

        queryset = Map.get_places(longitude, latitude, radius, Map.MapType.cloth)

        result = []
        for q in queryset:
            result.append([q.road_address, q.latitude, q.longitude])

        return Response(result, status=200)

    def post(self, request):
        serializer = MapSerilizer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(statis=201)

        return Response(status=400)
