from django.urls import path, include
from .get import export as GET_translations_get
from .list import export as GET_translations_list

urlpatterns = [
		path("<str:language>", view=GET_translations_get),
		path("list", view=GET_translations_list)
	]