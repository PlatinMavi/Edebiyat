from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse,JsonResponse
def get_api_versions(request):
    return JsonResponse((["/v1"]),safe=False)

urlpatterns = [
    path("",get_api_versions),
    path("v1/",include("api.v1")),
]