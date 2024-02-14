from django.shortcuts import render
from django.http import JsonResponse


def handler404(request):
    return render(request, "404.html", status=404)


def bad_request(request, exception, *args, **kwargs):
    """
    Generic 400 error handler.
    """
    data = {"error": "Bad Request (400)"}
    return JsonResponse(data, status=400)


def server_error(request, *args, **kwargs):
    data = {"error": "Server Error (500)"}
    print(data)
    return JsonResponse(data, status=500)
    return render(request, "500.html", status=500)
