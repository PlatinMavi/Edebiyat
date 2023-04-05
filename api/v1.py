from django.urls import path, include
from django.http import HttpResponse, JsonResponse, HttpRequest
from index.models import Kitap, Comment, Dergi, Siir, Yazar,filter_comment

def endpoint_comment_post(request:HttpRequest, id : int):
    if request.method.lower() != "post":
        return HttpResponse("Method Not Allowed!")
    if id == None:
        return HttpResponse("")
    is_hide_name = request.headers.get("is_hide_name")
    is_spoilers = request.headers.get("is_spoilers")
    author_name = request.headers.get("author_name")
    message = request.headers.get("author_name")
    headers = request.headers.__dict__

    return JsonResponse(True,safe=False)


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
