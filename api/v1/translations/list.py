from django.urls import path, include
from django.http import HttpResponse, JsonResponse, HttpRequest
import time
from util import error_response, can_be_restricted

from django.views.decorators.csrf import csrf_exempt

import os

@csrf_exempt
@can_be_restricted
def export(request: HttpRequest):
	return JsonResponse({"success":True,"data":{"tr":"Türkçe","en":"English"}}, safe=False)