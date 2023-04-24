from django.urls import path, include
from django.http import HttpResponse, JsonResponse, HttpRequest
from index.models import LiteratureObject, Comment, LiteratureObject, LiteratureObject, Creator, Vote, filter_comment
import time
from util import post_requests_only, error_response, get_requests_only

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@post_requests_only
def export(request: HttpRequest, object_id: int):
	if object_id == None:
		return HttpResponse("")
	headers = request.headers.__dict__
	is_hide_name = request.headers.get("is-hide-name")
	is_spoilers = request.headers.get("is-spoilers")
	author_name = request.headers.get("author-name")
	content = request.headers.get("content")
	if str(is_hide_name).lower() == "true":
		is_hide_name = True
	else:
		is_hide_name = False

	if str(is_spoilers).lower() == "true":
		is_spoilers = True
	else:
		is_spoilers = False

	if not content or len(content) < 1 or len(content) > 1000:
		return error_response("errors.comments.post.length", f"Comment length should be between 1 and 1000, got {content and len(content) or 'null'}")
	if not author_name or len(author_name) > 30 or len(author_name) < 3:
		return error_response("errors.comments.post.author.name", f"Author name should be between 3 and 30, got {author_name and len(author_name) or 'null'}")
	content = filter_comment(content)
	# got all parameters
	# now we can create comment
	# first we need to get parent object
	parent_object = LiteratureObject.objects.get(id=object_id)
	if not parent_object:
		return error_response("errors.comments.post.parent_object", f"Parent object not found with id {object_id}")
	# now we can create comment
	content = Comment(parent_object=parent_object, author_name=author_name, content=content, hide_name=is_hide_name,
					  spoilers=is_spoilers, author_ip=request.META.get("REMOTE_ADDR"), author_headers=headers,
					  author_id=request.META.get("REMOTE_ADDR")[:2])
	content.save()
	return JsonResponse(content.filtered_content(), safe=False)