from django.db import models

# Create your models here.
class Dergi(models.Model):
    isim = models.CharField(max_length=255)

    yayinci = models.CharField(max_length=255)
    foto = models.ImageField(upload_to="foto", default = "foto/noimage.png")
    url = models.URLField()

class Kitap(models.Model):
    isim = models.CharField(max_length=255)
    yazar = models.CharField(max_length=255)
    foto = models.ImageField(upload_to="foto", default = "foto/noimage.png")
    acikama = models.CharField(max_length=512, null=True)

class Siir(models.Model):
    isim = models.CharField(max_length=255)
    yazar = models.CharField(max_length=255)
    siir = models.TextField(max_length=512)

class Yazar(models.Model):
    isim = models.CharField(max_length=255)
    dt = models.DateField()
    foto = models.ImageField(upload_to="foto", default = "foto/noimage.png")
