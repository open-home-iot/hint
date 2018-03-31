from django.conf.urls import url

from surveillance.views import list_pictures


urlpatterns = [
    url(r'pictures', list_pictures),
]
