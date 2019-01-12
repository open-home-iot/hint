from django.urls import path

from .views import attach


urlpatterns = [
    path("attach", attach),
]
