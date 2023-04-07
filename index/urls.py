from django.urls import path, include
from . import views
from django.contrib import admin
urlpatterns = [
    path("", views.index, name= "index"),
    path("books/",include("books.urls")),
    path("api/",include("api.urls")),
    path('admin/', admin.site.urls),
]