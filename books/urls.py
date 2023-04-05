from django.urls import path

from . import views

urlpatterns = [
    path("<str:id>", view=views.render_book),
    path("",view=views.invalid_book)
]