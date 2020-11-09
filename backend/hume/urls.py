from django.urls import path

from backend.hume.views import Humes, HumeFind, HumeConfirmPairing


urlpatterns = [
    path("", Humes.as_view()),
    path("<str:hume_uuid>", HumeFind.as_view()),
    path("<str:hume_uuid>/confirm-pairing", HumeConfirmPairing.as_view())
]
