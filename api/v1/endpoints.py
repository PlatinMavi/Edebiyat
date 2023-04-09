from django.urls import path, include
urlpatterns = [
	path("literature_objects/", include("api.v1.literature_objects.__init__"))
]
