from django.shortcuts import render
from django.http import JsonResponse


def handler404(request):
    return render(request, "404.html", status=404)


def bad_request(request, exception, *args, **kwargs):
    data = {"error": str(exception)}
    return JsonResponse(data, status=400)


def server_error(request, *args, **kwargs):
    data = {"error": "Server Error (500)"}
    return JsonResponse(data, status=500)
