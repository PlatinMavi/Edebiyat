from django.urls import path, include
from django.http import HttpResponse, JsonResponse, HttpRequest
from index.models import Kitap, Comment, Dergi, Siir, Yazar, filter_comment
import time


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def endpoint_comment_post(request: HttpRequest, id: int):
    # if request.method.lower() != "post":
    # return error_response("errors.request.method_not_allowed",f"{request.method.upper()} requests to this endpoint is not allowed")
    if id == None:
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
    parent_object = Kitap.objects.get(id=id)
    if not parent_object:
        return error_response("errors.comment.post.parent_object", f"Book object not found with id {id}")
    # now we can create comment
    comment = Comment(parent=parent_object.id, author_name=author_name, message=comment, approved_by="Bilinmiyor", hide_name=is_hide_name,
                    spoilers=is_spoilers, author_ip=request.META.get("REMOTE_ADDR"), author_headers=headers,
                    author_id=request.META.get("REMOTE_ADDR")[:2])
    comment.save()
    return JsonResponse(comment.__str__(), safe=False)


def error_response(error_name: str, error_details: str = ""):
    return JsonResponse(
        {"success": False, "error": error_name or "",
         "error_details": error_details, "time": time.time()}
    )


@csrf_exempt
def endpoint_comment_list(request, id):
    return JsonResponse(
        [{
            "id": comment.id,
            "message": comment.message,
            "parent_object": comment.parent,
            "created_at": comment.created_at,
            "approved_by": comment.approved_by,
            "is_hide_name": comment.hide_name,
            "is_spoilers": comment.spoilers,
            "author": {"name": comment.hide_name and "Anonim" or comment.author_name, "id": comment.author_id},
        } for comment in Comment.objects.filter(parent=id)
        ], safe=False)


@csrf_exempt
def endpoint_list(request):
    return JsonResponse([{
        "book": {
            "name": kitap.isim,
            "image": kitap.foto,
            "description": kitap.aciklama
        },
        "author": {"name": kitap.yazar},

    } for kitap in Kitap.objects.all()])


class ENDPOINTS:
    BOOKS = [
        path("<int:id>/comments/post", view=endpoint_comment_post),
        path("<int:id>/comments/list", view=endpoint_comment_list),
        path("list", view=endpoint_list)
    ]


urlpatterns = [
    path("books/", include(ENDPOINTS.BOOKS))
]
