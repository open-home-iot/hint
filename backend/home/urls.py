from django.urls import path

from backend.home.views import Homes, HomeRooms
from backend.hume.views import HomeHumes


urlpatterns = [
    path("", Homes.as_view()),
    # This is just to make it more readable and a more logical API, request ALL
    # HUMEs for a given home: /api/home/humes. Otherwise it will be cumbersome
    # to query for. Should create similar API view for devices of a given HUME.
    # Still, the view needs to enforce strict user checks to make sure some
    # other user is not querying for another user's HUMEs.
    path("<int:home_id>/humes", HomeHumes.as_view()),
    path("<int:home_id>/rooms", HomeRooms.as_view())
]
