from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.v1.serializer_without_model.serializer import (
    PlantSerializer,
    InverterSerializer,
    EssSerializer,
)


class IntegrationApiView(APIView):
    def post(self, request, type):
        if type.lower() not in ["plant", "inverter", "ess"]:
            return Response(status=400)

        if type == "plant":
            plant_serializer = PlantSerializer(data=request.data)
            plant_serializer.is_valid(raise_exception=True)
        elif type == "inverter":
            inverter_serializer = InverterSerializer(data=request.data, many=True)
            inverter_serializer.is_valid(raise_exception=True)
        elif type == "ess":
            ess_serializer = EssSerializer(data=request.data, many=True)
            ess_serializer.is_valid(raise_exception=True)

        return Response(status=status.HTTP_200_OK)
