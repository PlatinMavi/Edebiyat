from django.contrib import admin

# Register your models here.
from .models import LiteratureObject, Creator,Comment, Vote
admin.site.register(LiteratureObject)
admin.site.register(Creator)
admin.site.register(Comment)
admin.site.register(Vote)