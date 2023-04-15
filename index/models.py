from django.db import models
# Create your models here.

class VoteableObject(models.Model):
	class Meta:
		abstract = True
	down_votes = models.IntegerField(default=0, editable=True)
	up_votes = models.IntegerField(default=0, editable=True)
	def ADD_VOTE(self, value: int, ip:str):
		if not (value in [-1,0,1]):
			return
		target_object_type = type(self).__name__
		vote = Vote.objects.get_or_create(ip_adress=ip, parent_literature_object = target_object_type == "LiteratureObject" and self or None, parent_comment = target_object_type == "Comment" and self or None)[0]
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
		self.CALCULATE_INTEREST_RATE()
		vote.save()
		self.save()
	interest_rate = models.FloatField(default=0, editable=False)
	def CALCULATE_INTEREST_RATE(self):
		self.interest_rate = (self.up_votes - self.down_votes)
		self.save()
	def GET_VOTE_COUNT(self):
		self.CALCULATE_INTEREST_RATE()
		return {"up":self.up_votes, "down":self.down_votes}
class Creator(models.Model):
	ObjectIndexes = ["writer","publisher"]
	ObjectTypes = [("writer","Yazar"),("publisher","Yayımcı")]
	name = models.CharField(max_length=255)
	created_at = models.DateField()
	image = models.ImageField(upload_to="foto", default="foto/noimage.png")
	type = models.CharField(choices=ObjectTypes, default = "writer", max_length=255)
	def __str__(self):
		return f"{self.id} : ({self.ObjectTypes[self.ObjectIndexes.index(self.type)][1]}) {self.name}"

class LiteratureObject(VoteableObject):
	ObjectIndexes = ["book","magazine","poem"]
	ObjectTypes = [("book","Kitap"),("magazine","Dergi"),("poem","Şiir")]
	name = models.CharField(verbose_name= "İsim", max_length=255)
	creator = models.ForeignKey(Creator,verbose_name="Yazar / Yayıncı", default=None,on_delete=models.DO_NOTHING)
	image = models.ImageField(verbose_name="Fotoğraf", upload_to="foto", default="foto/noimage.png")
	url = models.URLField(verbose_name="Esere ait link")
	content = models.TextField(verbose_name="İçerik" , max_length=1000)
	type = models.TextField(verbose_name="Tür", choices = ObjectTypes)
	# interest_rate = models.FloatField(verbose_name="İlgi Oranı", default=0)
	def __str__(self):
		return f"{self.id} : ({self.creator.ObjectTypes[self.creator.ObjectIndexes.index(self.creator.type)][1]}) {self.creator.name} : ({self.ObjectTypes[self.ObjectIndexes.index(self.type)][1]}) {self.name}"
	def GetComments(self):
		return Comment.objects.filter(parent_object=self).all()
	# def RefreshInterestRate(self):
	# 	comments = self.GetComments()
	# 	total_comments = len(comments)
	# 	for comment in comments:
	# 		votes = comment.GET_VOTE_COUNT()
	# 		comment_interest_rate = votes["up"]-votes["down"]
	# 		total_votes = votes["up"]-votes["down"]
	# 		self.interest_rate = total_votes/total_comments
	def filtered_content(self) -> str:
		return {
			"id":self.id,
			"type":self.type,
			"url":self.url,
			"name":self.name,
			"image": {"url": self.image.url, "width": self.image.width, "height": self.image.height},
			"creator":{"id":self.creator.id,"name":self.creator.name},
			"votes":self.GET_VOTE_COUNT(),
			"content":self.content,
			"comment_count":len(self.GetComments()),
			"interest_rate":self.interest_rate
		}

class Comment(VoteableObject):
	parent_object = models.ForeignKey(LiteratureObject,on_delete=models.CASCADE, 
		editable=False, verbose_name="Yorum Yapılan Eser", default=0)
	author_name = models.CharField(max_length=30, verbose_name="Kullanıcı Adı")
	message = models.TextField(max_length=1000, verbose_name="Yorum İçeriği")
	created_at = models.DateField(auto_now=True, editable=False)
	approved_by = models.CharField(choices=((None,"None"),("phasenull","phasenull"),("admin","admin")),
		max_length=30, default=None, editable=True, verbose_name="Onaylayan Yetkili", null=True, blank=True)
	hide_name = models.BooleanField(
		default=False, verbose_name="Yazar İsmini Gizle", editable=True)
	spoilers = models.BooleanField(
		verbose_name="Mesaj Spoiler İçeriyor", default=False)
	author_ip = models.CharField(editable=False, max_length=30)
	author_headers = models.CharField(
		editable=False, max_length=1000, default="?")
	author_id = models.CharField(max_length=3,editable=False, default=-1,null=True)
	def filtered_content(self) -> str:
		return {
				"id":self.id,
				"parent_object":{"id":self.parent_object.id},
				"author": {"name": self.hide_name and None or self.author_name, "uid": self.author_id},
				"created_at":self.created_at,
				"vote_count":self.GET_VOTE_COUNT(),
				"approved_by":self.approved_by,
				"hide_name":self.hide_name,
				"spoilers":self.spoilers,
				"message":self.message,
			}
	def __str__(self) -> str:
		literature_object = LiteratureObject.objects.filter(id=self.parent_object.id).first()
		literature_object = literature_object and literature_object.name or "hatalı_eser"
		var_0 = not self.approved_by and '(onaylanmamış) : '
		return f"{var_0 or ''}{self.id} : {literature_object} : {self.author_name} : {self.approved_by or '-'}"


class Vote(models.Model):
	ip_adress = models.GenericIPAddressField(editable=True,default="0.0.0.0",null=False)
	value = models.IntegerField(default=0, editable=True)
	parent_object_type = models.TextField(choices=(("a","Yorum"),("b","Eser")),default="a",editable=True)
	# _parent_object_type = parent_object_type == Comment and Comment or LiteratureObject
	parent_comment = models.ForeignKey(Comment,on_delete=models.CASCADE,editable=True,null=True,blank=True)
	parent_literature_object = models.ForeignKey(LiteratureObject,on_delete=models.CASCADE,editable=True,null=True,blank=True)
	def IS_UP(self) -> bool:
		return self.value == 1
	def IS_DELETE(self) -> bool:
		return self.value == 0
	def IS_DOWN(self) -> bool:
		return self.value == -1

def filter_comment(comment: Comment):
	return comment
