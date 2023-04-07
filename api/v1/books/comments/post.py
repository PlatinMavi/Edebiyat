from django.urls import path, include
from django.http import HttpResponse, JsonResponse, HttpRequest
from index.models import Kitap, Comment, Dergi, Siir, Yazar, Vote, filter_comment
import time
from util import post_requests_only, error_response, get_requests_only

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@post_requests_only
def export(request: HttpRequest, book_id: int):
	if book_id == None:
		return HttpResponse("")
	headers = request.headers.__dict__
	is_hide_name = request.headers.get("is-hide-name")
	is_spoilers = request.headers.get("is-spoilers")
	author_name = request.headers.get("author-name")
	comment = request.headers.get("comment")
	if str(is_hide_name).lower() == "true":
		is_hide_name = True
	else:
		is_hide_name = False

	if str(is_spoilers).lower() == "true":
		is_spoilers = True
	else:
		is_spoilers = False

	if not comment or len(comment) < 20 or len(comment) > 1000:
		return error_response("errors.comment.post.length", f"Comment length should be between 20 and 1000, got {comment and len(comment) or 'null'}")
	if not author_name or len(author_name) > 30 or len(author_name) < 3:
		return error_response("errors.comment.post.author.name", f"Author name should be between 3 and 30, got {author_name and len(author_name) or 'null'}")
	comment = filter_comment(comment)
	# got all parameters
	# now we can create comment
	# first we need to get parent object
	parent_object = Kitap.objects.get(id=book_id)
	if not parent_object:
		return error_response("errors.comment.post.parent_object", f"Book object not found with id {book_id}")
	# now we can create comment
	comment = Comment(parent_object=parent_object.id, author_name=author_name, message=comment, approved_by="Bilinmiyor", hide_name=is_hide_name,
					  spoilers=is_spoilers, author_ip=request.META.get("REMOTE_ADDR"), author_headers=headers,
					  author_id=request.META.get("REMOTE_ADDR")[:2])
	comment.save()
	return JsonResponse(comment.tostring(), safe=False)