from django.urls import path, include
from django.http import HttpResponse, JsonResponse, HttpRequest
from index.models import LiteratureObject, Comment, LiteratureObject, LiteratureObject, Creator, Vote, filter_comment
import time
from util import post_requests_only, error_response, can_be_restricted

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@can_be_restricted
def export(request: HttpRequest):
    ACCEPT_MAX_RESULTS = [0, 1, 5, 10, 20, 50]
    try:
        cursor = request.GET.get("cursor") and int(
            request.GET.get("cursor")) or 0
        if cursor < 0:
            raise Exception("errors.comments.list.cursor")
    except:
        return error_response("errors.comments.list.cursor", f"Cursor must be an integer bigger or equal to 0, got {request.GET.get('cursor')}")
    try:
        max_results = (request.GET.get("max-results")
                       and int(request.GET.get("max-results"))) or 0
        if max_results and not (max_results in ACCEPT_MAX_RESULTS):
            raise Exception("errors.comments.list.max_results")
    except Exception as e:
        # return HttpResponse(e)
        return error_response("errors.comment.list.cursor.max-results", f"Max results must be one of {ACCEPT_MAX_RESULTS}, got {request.GET.get('max-results')}")
    return JsonResponse({
		"success":True,
        "data": [literature_object.filtered_content() for literature_object in LiteratureObject.objects.order_by("id")[cursor*max_results:(cursor+1)*max_results]]
        }, safe=False)
