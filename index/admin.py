from django.contrib import admin

# Register your models here.
from .models import Siir, Kitap, Dergi, Yazar,Comment
admin.site.register(Siir)
admin.site.register(Kitap)
admin.site.register(Dergi)
admin.site.register(Yazar)
admin.site.register(Comment)