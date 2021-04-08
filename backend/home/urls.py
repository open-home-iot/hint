from django.urls import path

from backend.home.views import Homes, HomeRooms
from backend.hume.views import HomeHumes
from backend.device.views import RoomDevices, HomeDevices


home_urls = [
    path("", Homes.as_view()),

    # TODO: decide if API paths shall be revamped to a longer but more
    #       logical form, examples below
    #  /api/homes/<id>/rooms/<id>/devices
    #  /api/homes/<id>/rooms/<id>/devices/<uuid>
    #  /api/homes/<id>/humes
    #  /api/homes/<id>/humes/<uuid>
    path("<int:home_id>/humes", HomeHumes.as_view()),
    path("<int:home_id>/rooms", HomeRooms.as_view()),

    path("<int:home_id>/devices", HomeDevices.as_view())
]

room_urls = [
    path("<int:room_id>/devices", RoomDevices.as_view())
]
