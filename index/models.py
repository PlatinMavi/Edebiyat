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
	
	parent_object = models.IntegerField(
		editable=False, verbose_name="Yorum Yapılan Eser Numarası", default=0)
	author_name = models.CharField(max_length=30, verbose_name="Kullanıcı Adı")
	message = models.TextField(max_length=1000, verbose_name="Yorum İçeriği")
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
	up_votes = models.IntegerField(default=0, editable=True)
	down_votes = models.IntegerField(default=0, editable=True)
	def ADD_VOTE(self, value: int, ip:str):
		if not (value in [-1,0,1]):
			return
		vote = Vote.objects.get_or_create(ip_adress=ip, parent_comment = self)[0]
		print(vote.__dict__)
		if vote:
			# delete old votes
			if vote.IS_UP():
				self.up_votes -= 1
			elif vote.IS_DOWN():
				self.down_votes -= 1
		vote.value = value
		if vote.IS_UP():
			self.up_votes += 1
		elif vote.IS_DOWN():
			self.down_votes += 1
		vote.save()
		self.save()

	def GET_VOTE_COUNT(self):
		return {"up":self.up_votes, "down":self.down_votes}

	def tostring(self) -> str:
		return str({
			"id":self.id,
			"parent":self.parent_object,
			"author_name":self.author_name,
			"message":self.message,
			"created_at":self.created_at,
			"approved_by":self.approved_by,
			"hide_name":self.hide_name,
			"spoilers":self.spoilers,
			"author_ip":self.author_ip,
			"author_headers":self.author_headers,
			"author_id":self.author_id,
			"vote_count":self.GET_VOTE_COUNT(),
			})
	def __str__(self) -> str:
		name = Kitap.objects.get(id=self.parent_object)
		name = name and name.isim or "Bilinmeyen Kitap"
		return f"{self.id} : {name} : {self.author_name}"


class Vote(models.Model):
	ip_adress = models.GenericIPAddressField(editable=True,default="0.0.0.0",null=False)
	value = models.IntegerField(default=0, editable=True)
	parent_comment = models.ForeignKey(Comment,on_delete=models.CASCADE,editable=True,null=models.CASCADE)
	def IS_UP(self) -> bool:
		return self.value == 1
	def IS_DELETE(self) -> bool:
		return self.value == 0
	def IS_DOWN(self) -> bool:
		return self.value == -1

def filter_comment(comment: Comment):
	return comment
