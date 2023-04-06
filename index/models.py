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
	parent = models.IntegerField(
		editable=False, verbose_name="Yorum Yapılan Eser Numarası", default=0)
	author_name = models.CharField(max_length=30, verbose_name="Kullanıcı Adı")
	message = models.CharField(max_length=1000, verbose_name="Mesaj")
	created_at = models.DateField(auto_now=True, editable=False)
	approved_by = models.CharField(
		max_length=30, default="Bilinmiyor", editable=True, verbose_name="Onaylayan Yetkili")
	hide_name = models.BooleanField(
		default=False, verbose_name="Yazar İsmini Gizle", editable=True)
	spoilers = models.BooleanField(
		verbose_name="Mesaj Spoiler İçeriyor", default=False)
	author_ip = models.CharField(editable=False, max_length=30)
	author_headers = models.CharField(
		editable=False, max_length=1000, default="?")
	author_id = models.CharField(max_length=3,editable=False, default=-1,null=True)
	def __str__(self) -> str:
		return str({
			"id":self.id,
			"parent":self.parent,
			"author_name":self.author_name,
			"message":self.message,
			"created_at":self.created_at,
			"approved_by":self.approved_by,
			"hide_name":self.hide_name,
			"spoilers":self.spoilers,
			"author_ip":self.author_ip,
			"author_headers":self.author_headers,
			"author_id":self.author_id
			})


def filter_comment(comment: Comment):
	return comment
