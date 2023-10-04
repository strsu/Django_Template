from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Sum, F

from .models import Price


class PriceApiView(APIView):
    def get(self, request):
        date = request.GET.get("date")
        time = request.GET.get("time")

        result = (
            Price.objects.filter(date=date, time=time)
            .values("date", "time")
            .annotate(total_values=Sum("values"))
        )

        return Response(result, status=200)

    def post(self, request):
        date = request.data.get("date")
        time = request.data.get("time")
        price = request.data.get("price")

        Price.objects.create(date=date, time=time, values=price)

        return Response(status=201)
