from django import shortcuts
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

# Create your views here.
from index.models import LiteratureObject,LiteratureObject,LiteratureObject,Creator
def render_book(request,id : str or None):
    template = loader.get_template("book_details.html")

    kitap_query = LiteratureObject.objects.filter(id=id)
    if (len(kitap_query) == 0):
        return page_not_found()
    data = {"BOOK" : kitap_query[0]}
    return HttpResponse(template.render(data,request))

def page_not_found():
    return HttpResponse("Error: 404",status=404)


def invalid_book(request):
    return page_not_found()
    # template = loader.get_template("book_details.html")
    # data = {"BOOK" : {
    #     "isim":"lorem ipsum",
    #     "yazar":"UNKNOWN",
    #     "aciklama":"hello"
    # }}
    # return HttpResponse(template.render(data,request))