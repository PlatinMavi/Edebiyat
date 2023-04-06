from django.urls import path, include
from django.http import HttpResponse, JsonResponse, HttpRequest
from index.models import Kitap, Comment, Dergi, Siir, Yazar,filter_comment
import time
def endpoint_comment_post(request:HttpRequest, id : int):
    if request.method.lower() != "post":
        return HttpResponse("Method Not Allowed!")
    if id == None:
        return HttpResponse("")
    is_hide_name = request.headers.get("is_hide_name").lower()
    is_spoilers = request.headers.get("is_spoilers").lower()
    author_name = request.headers.get("author_name")
    message = request.headers.get("author_name")
    headers = request.headers.__dict__
    if not (is_hide_name in ("true","false")):
        is_hide_name = False
    is_hide_name = bool(is_hide_name)
    
    if not (is_spoilers in ("true","false")):
        is_spoilers = False
    is_spoilers = bool(is_hide_name)
    
    if not message or len(message) < 20 or len(message) > 1000:
        return error_response(f"message length should be between 20 and 1000")
    if not author_name or len(author_name) < 30 or len(author_name) > 5:
        return error_response(f"author name should be between 5 and 30")

    return JsonResponse(True,safe=False)

def error_response(error_desc):
    return JsonResponse(
        {"success":False,"error":error_desc or "","time":time.time()}
    )

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
