from django.urls import path, include
urlpatterns = [
	path("books/", include("api.v1.books.__init__"))
]
