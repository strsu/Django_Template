from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response


class BlogApiView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_200_OK)
