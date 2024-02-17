from django.shortcuts import render
from django.http import JsonResponse

from django.http import HttpResponse


def handler404(request):
    return render(request, "404.html", status=404)


def bad_request(request, exception, *args, **kwargs):

    message = str(exception)
    # return Response(data, status=400)
    return HttpResponse(
        message, status=400, content_type="application/json; charset=utf-8"
    )


def server_error(request, *args, **kwargs):
    data = {"error": "Server Error (500)"}
    return JsonResponse(data, status=500)
