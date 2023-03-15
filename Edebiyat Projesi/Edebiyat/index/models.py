from django.db import models

# Create your models here.
class Dergi(models.Model):
    isim = models.CharField(max_length=255)
    yayinci = models.CharField(max_length=255)
    foto = models.ImageField(upload_to="foto", null=True)

class Kitap(models.Model):
    isim = models.CharField(max_length=255)
    yazar = models.CharField(max_length=255)
    foto = models.ImageField(upload_to="foto", null=True)

class Siir(models.Model):
    isim = models.CharField(max_length=255)
    yazar = models.CharField(max_length=255)
    foto = models.ImageField(upload_to="foto", null=True)

class Yazar(models.Model):
    isim = models.CharField(max_length=255)
    dt = models.DateField()
    foto = models.ImageField(upload_to="foto", null=True)
