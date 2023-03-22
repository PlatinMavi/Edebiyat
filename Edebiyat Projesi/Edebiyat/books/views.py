from django import shortcuts
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

# Create your views here.
from index.models import Dergi,Kitap,Siir,Yazar
def render_book(request,id : str or None):
    template = loader.get_template("book_details.html")

    kitap_query = Kitap.objects.filter(isim=id)
    if (len(kitap_query) == 0):
        return shortcuts.redirect("/books/Lorem%20Ipsum")
    data = {"BOOK" : kitap_query[0]}
    return HttpResponse(template.render(data,request))

def invalid_book(request):
    return shortcuts.redirect("/books/Lorem%20Ipsum")
    # template = loader.get_template("book_details.html")
    # data = {"BOOK" : {
    #     "isim":"lorem ipsum",
    #     "yazar":"UNKNOWN",
    #     "aciklama":"hello"
    # }}
    # return HttpResponse(template.render(data,request))