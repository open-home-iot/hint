from django.urls import path

from backend.hume.views import Humes, HumeFind, HumeAssociate, \
                               HumeConfirmPairing


urlpatterns = [
    path("", Humes.as_view()),
    path("<str:hume_uuid>", HumeFind.as_view()),
    path("<int:hume_id>/associate", HumeAssociate.as_view()),
    path("<int:hume_id>/confirm-pairing", HumeConfirmPairing.as_view()),
]
