from django.conf.urls import url

from backend.events.views import alarm


urlpatterns = [
    url(r'alarm', alarm)
]