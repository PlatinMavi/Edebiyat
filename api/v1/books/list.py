from django.urls import path, include
from django.http import HttpResponse, JsonResponse, HttpRequest
from index.models import Kitap, Comment, Dergi, Siir, Yazar, Vote, filter_comment
import time
from util import post_requests_only, error_response, get_requests_only

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@get_requests_only
def export(request: HttpRequest):
	cursor = request.GET.get("cursor") or 0
	max_results = request.GET.get("max-results") or 1
	return JsonResponse([{
		"name": kitap.isim,
		"image": {"url": kitap.foto.url, "width": kitap.foto.width, "height": kitap.foto.height},
		"description": kitap.acikama,
		"author": {"name": kitap.yazar},

	} for kitap in Kitap.objects.order_by("id")[cursor*max_results:(cursor+1)*max_results]], safe=False)