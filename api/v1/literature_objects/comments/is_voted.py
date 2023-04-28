from asyncio.windows_events import NULL
from genericpath import exists
from django.urls import path, include
from django.http import HttpResponse, JsonResponse, HttpRequest
from index.models import LiteratureObject, Comment, LiteratureObject, LiteratureObject, Creator, Vote, filter_comment
from util import post_requests_only, error_response, can_be_restricted, get_requests_only

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@get_requests_only
def export(request:HttpRequest, object_id, comment_id):
	final_id = comment_id
	try:
		comment_id = int(comment_id)
	except:
		return error_response(
			"errors.comments.vote.comment_id_invalid",
			f"Comment id must be an integer, got {comment_id}")
	if comment_id == -1:
		# vote to LiteratureObject
		comment = LiteratureObject.objects.filter(id=object_id).first()
		if not comment:
			return error_response(
				"errors.literature_objects.not_found",
				f"LiteratureObject not found with id {object_id}")
		final_id = object_id
	else:
		comment = Comment.objects.filter(id=comment_id).first()
		if not comment:
			return error_response(
				"errors.comments.not_found",
				f"Comment not found with id {comment_id}")
	vote = Vote.objects.filter(parent_comment = final_id,ip_adress=request.META.get("REMOTE_ADDR"))
	return JsonResponse({"success":True,"data":{"is_voted": vote.exists(),"value":vote.exists() and vote.first().value or 0}}, safe=False)