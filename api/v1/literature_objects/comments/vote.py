from django.urls import path, include
from django.http import HttpResponse, JsonResponse, HttpRequest
from index.models import LiteratureObject, Comment, LiteratureObject, LiteratureObject, Creator, Vote, filter_comment
import time
from util import post_requests_only, error_response, get_requests_only

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@post_requests_only
def export(request, object_id, comment_id):
	try:
		comment_id = int(comment_id)
	except:
		return error_response(
			"errors.comments.vote.comment_id_invalid",
			f"Comment id must be an integer, got {comment_id}")
	vote_value = request.headers.get("vote-value")
	if not vote_value:
		return error_response(
			"errors.comments.vote.value_expected",
			f"vote-value header is required")
	if not (vote_value in ("1", "-1", "0")):
		return error_response(
			"errors.comments.vote.value_invalid",
			f"vote-value header should be 1, -1 or 0, got {vote_value}")
	vote_value = int(vote_value)
	if comment_id == -1:
		# vote to LiteratureObject
		comment = LiteratureObject.objects.filter(id=object_id).first()
		if comment:
			vote = comment.ADD_VOTE(vote_value, request.META.get("REMOTE_ADDR"))
		else:
			return error_response(
				"errors.literature_objects.not_found",
				f"LiteratureObject not found with id {object_id}")
	else:
		comment = Comment.objects.filter(id=comment_id).first()
		if not comment:
			return error_response(
				"errors.comments.not_found",
				f"Comment not found with id {comment_id}")
	comment.ADD_VOTE(vote_value, request.META.get("REMOTE_ADDR"))
	return JsonResponse({"votes": comment.GET_VOTE_COUNT(), "comment_id": comment.id}, safe=False)