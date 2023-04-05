from tabnanny import verbose
from django.db import models

# Create your models here.


class Dergi(models.Model):
    isim = models.CharField(max_length=255)

    yayinci = models.CharField(max_length=255)
    foto = models.ImageField(upload_to="foto", default="foto/noimage.png")
    url = models.URLField()


class Kitap(models.Model):
    isim = models.CharField(max_length=255)
    yazar = models.CharField(max_length=255)
    foto = models.ImageField(upload_to="foto", default="foto/noimage.png")
    acikama = models.CharField(max_length=512, null=True)


class Siir(models.Model):
    isim = models.CharField(max_length=255)
    yazar = models.CharField(max_length=255)
    siir = models.TextField(max_length=512)


class Yazar(models.Model):
    isim = models.CharField(max_length=255)
    dt = models.DateField()
    foto = models.ImageField(upload_to="foto", default="foto/noimage.png")


class Comment(models.Model):
    id = models.IntegerField(editable=False, primary_key=True)
    parent = models.IntegerField(
        editable=False, verbose_name="Yorum Yapılan Eser Numarası", default=0)
    author_name = models.CharField(max_length=30, verbose_name="Kullanıcı Adı")
    message = models.CharField(max_length=1000, verbose_name="Mesaj")

    created_at = models.DateField(auto_now=True, editable=False)
    approved_by = models.CharField(
    max_length=30, default="Bilinmiyor", editable=True, verbose_name="Onaylayan Yetkili")
    hide_name = models.BooleanField(
    default=False, verbose_name="Yazar İsmini Gizle", editable=True)
    spoilers = models.BooleanField(verbose_name="Mesaj Spoiler İçeriyor", default=False)
    author_ip = models.CharField(editable=False, max_length=30)
    author_headers = models.CharField(editable=False, max_length=1000,default="?")

def filter_comment(comment:Comment):
    return comment