from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Yazar,Kitap,Dergi,Siir
import datetime

# Create your views here.
def index(request):

    dergi = Dergi.objects.all()[:5]
    kitap = Kitap.objects.all()[:5]
    siir = Siir.objects.all()[0]
    aykitap = Kitap.objects.all()[0]

    zaman = datetime.datetime.now()
    zaman = zaman.strftime("%m")
    aylar = ["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]
    buay = aylar[int(zaman)-1]
    yazar = Yazar.objects.all().filter(dt__month=zaman)
    yazar1 = yazar[:5]
    yazar2 = yazar[5:10]

    template = loader.get_template("index.html")
    context={
        "DERGI":dergi,
        "KITAP":kitap,
        "YAZAR1":yazar1,
        "YAZAR2":yazar2,
        "SIIR":siir,
        "AY":buay,
        "AYKITAP":aykitap,
    }
    return HttpResponse(template.render(context, request))