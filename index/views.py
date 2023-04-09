from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Creator,LiteratureObject,LiteratureObject,LiteratureObject
import datetime

# Create your views here.
def index(request):

    dergi = LiteratureObject.objects.filter(type="magazine").all().first()
    kitap = LiteratureObject.objects.filter(type="book").all().first()
    siir = LiteratureObject.objects.filter(type="poem").all().first()
    aykitap = LiteratureObject.objects.all().order_by("interest_rate").last()
    zaman = datetime.datetime.now()
    zaman_str = zaman.strftime("%Y-%m-%d")
    aylar = ["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]
    buay = aylar[int(zaman.month)-1]
    yazar = Creator.objects.all().filter(created_at=zaman)
    yazar1 = yazar[:5]
    yazar2 = yazar[5:10]
    template = loader.get_template("index.html")
    context={
        "DERGI":dergi and dergi.filtered_json(),
        "KITAP":kitap and kitap.filtered_json(),
        "YAZAR1":yazar1,
        "YAZAR2":yazar2,
        "SIIR":siir and siir.filtered_json(),
        "AY":buay,
        "AYKITAP": aykitap and siir.filtered_json(),
    }
    return HttpResponse(template.render(context, request))
