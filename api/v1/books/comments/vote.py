from django.urls import path, include
from django.http import HttpResponse, JsonResponse, HttpRequest
from index.models import LiteratureObject, Comment, LiteratureObject, LiteratureObject, Creator, Vote, filter_comment
import time
from util import post_requests_only, error_response, get_requests_only

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@post_requests_only
def export(request, book_id, comment_id):
	vote_value = request.headers.get("vote-value")
	if not vote_value:
		return error_response("errors.comment.vote.value_expected", f"Vote value is required")
	if not (vote_value in ("1", "-1", "0")):
		return error_response("errors.comment.vote.value_invalid", f"Vote value should be 1, -1 or 0, got {vote_value}")
	vote_value = int(vote_value)
	comment = Comment.objects.get(id=comment_id)
	if not comment:
		return error_response("errors.comment.not_found", f"Comment not found with id {comment_id}")
	comment.ADD_VOTE(vote_value, request.META.get("REMOTE_ADDR"))
	return JsonResponse({"votes": comment.GET_VOTE_COUNT(), "comment_id": comment.id}, safe=False)