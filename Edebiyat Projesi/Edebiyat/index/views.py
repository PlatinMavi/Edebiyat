from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Yazar,Kitap,Dergi,Siir

# Create your views here.
def index(request):

    dergi = Dergi.objects.all()
    kitap = Kitap.objects.all()
    yazar = Yazar.objects.all()
    siir = Siir.objects.all()


    template = loader.get_template("index/index.html")
    context={
        "DERGI":dergi,
        "KITAP":kitap,
        "YAZAR":yazar,
        "SIIR":siir,
    }
    return HttpResponse(template.render(context, request))