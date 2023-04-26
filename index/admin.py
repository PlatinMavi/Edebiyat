from django.contrib import admin
@admin.action(description="Yorumları Toplu Onayla")
def bulk_approve(modeladmin, request, queryset):
    queryset.update(approved_by = "admin")
# Register your models here.
from .models import LiteratureObject, Creator,Comment, Vote
class CommentsAdmin(admin.ModelAdmin):
    actions = [bulk_approve]
admin.site.register(LiteratureObject)
admin.site.register(Creator)
admin.site.register(Comment,CommentsAdmin)
admin.site.register(Vote)