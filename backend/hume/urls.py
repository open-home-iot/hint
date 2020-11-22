from django.urls import path

from backend.hume.views import Humes, HumeFind, HumeConfirmPairing, \
    BrokerCredentials


urlpatterns = [
    # NOT AJAX
    path("", Humes.as_view()),
    path("broker-credentials", BrokerCredentials.as_view()),

    # AJAX
    path("<str:hume_uuid>", HumeFind.as_view()),
    path("<str:hume_uuid>/confirm-pairing", HumeConfirmPairing.as_view())
]
