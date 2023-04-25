from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Creator,LiteratureObject,LiteratureObject,LiteratureObject
import datetime

# Create your views here.
def index(request):

    magazines = LiteratureObject.objects.filter(type="magazine").all()
    books = LiteratureObject.objects.filter().all() # type="book"
    top_poem = LiteratureObject.objects.filter(type="poem").all().first()
    book_of_the_month = LiteratureObject.objects.all().order_by("interest_rate").last()
    zaman = datetime.datetime.now()
    zaman_str = zaman.strftime("%Y-%m-%d")
    aylar = ["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]
    this_month = aylar[int(zaman.month)-1]
    birthday_creator = Creator.objects.all().filter(created_at__month=zaman.month, type = "writer").order_by("created_at")
    template = loader.get_template("index.html")
    context={
        "TOP_MAGAZINES": magazines and [magazine.filtered_content() for magazine in magazines],
        "TOP_POEM": top_poem and top_poem.filtered_content(),
        "TOP_BOOKS": books and [book.filtered_content() for book in books],
        "CREATOR_BIRTHDAY": birthday_creator,
        "THIS_MONTH": this_month,
        "BOOK_OF_THE_MONTH": book_of_the_month and top_poem.filtered_content(),
    }
    return HttpResponse(template.render(context, request))
