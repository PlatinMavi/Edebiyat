from django.urls import path, include
from django.http import HttpResponse, JsonResponse, HttpRequest
from index.models import LiteratureObject, Comment, LiteratureObject, LiteratureObject, Creator, Vote, filter_comment
import time
from util import post_requests_only, error_response, get_requests_only

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@get_requests_only
def export(request, book_id):
	ACCEPT_MAX_RESULTS = [0, 1, 5, 10, 20, 50]
	try:
		cursor = request.GET.get("cursor") and int(request.GET.get("cursor")) or 0
		if cursor < 0:
			raise Exception("cursor < 0")
	except:
		return error_response("errors.comment.list.cursor", f"Cursor must be an integer bigger or equal to 0, got {request.GET.get('cursor')}")
	try:
		max_results = (request.GET.get("max-results") and int(request.GET.get("max-results"))) or 0
		if max_results and not (max_results in ACCEPT_MAX_RESULTS):
			raise Exception("max-results not in ACCEPT_MAX_RESULTS")
	except Exception as e:
		# return HttpResponse(e)
		return error_response("errors.comment.list.invalid_max-results", f"Max results must be one of {ACCEPT_MAX_RESULTS}, got {request.GET.get('max-results')}")
	return JsonResponse(
		[{
			"id": comment.id,
			"message": comment.message,
			"parent_object": comment.parent_object,
			"created_at": comment.created_at,
			"approved_by": comment.approved_by,
			"is_hide_name": comment.hide_name,
			"is_spoilers": comment.spoilers,
			"vote_count": comment.GET_VOTE_COUNT(),
			"author": {"name": comment.hide_name and "Anonim" or comment.author_name, "id": comment.author_id},
		} for comment in Comment.objects.filter(parent_object=book_id).order_by("id")[cursor*max_results:(cursor+1)*max_results]], safe=False)
