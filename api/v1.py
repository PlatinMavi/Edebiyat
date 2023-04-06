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
    is_hide_name = request.headers.get("is_hide_name")
    is_spoilers = request.headers.get("is_spoilers")
    author_name = request.headers.get("author_name")
    comment = request.headers.get("comment")
    headers = request.headers.__dict__
    is_hide_name = is_hide_name or False
    is_spoilers = is_spoilers or False
    if not (str(is_hide_name).lower() in ("true", "false")):
        is_hide_name = False
    is_hide_name = bool(is_hide_name)

    if not (str(is_spoilers).lower() in ("true", "false")):
        is_spoilers = False
    is_spoilers = bool(is_hide_name)

    if not comment or len(comment) < 20 or len(comment) > 1000:
        return error_response("errors.comment.post.length",f"comment length should be between 20 and 1000, got {comment and len(comment) or 'null'}")
    if not author_name or len(author_name) > 30 or len(author_name) < 5:
        return error_response("errors.comment.post.author.name",f"author name should be between 5 and 30, got {author_name and len(author_name) or 'null'}")

    return JsonResponse(True, safe=False)


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
            "author": {"name": comment.author_name},
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
