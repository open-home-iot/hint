from django.urls import path, include

from django.contrib import admin
from django.http import JsonResponse
from rest_framework import status

from backend.home.views import Homes, HomeRooms
from backend.device.views import (
    Devices,
    HomeDevices,
    DeviceAction,
    RoomDevices,
    ChangeDeviceRoom
)
from backend.hume.views import (
    HomeHumes,
    HumeAttachDevice,
    HumeDiscoverDevices,
    Humes,
    BrokerCredentials,
    HumeFind,
    HumeConfirmPairing
)
from backend.user.views import UserSignup, login_user, logout_user, UserSelf

from backend.webapp.views import AppView


def api_path_not_found(_request, url=None):
    """
    Returns a base 404 message and status for all API calls that lead nowhere.

    :param _request:
    :param url: URL that had no match
    :return:
    """
    print(f"API URL: {url} does not exist!")
    return JsonResponse({"error": "Resource not found."},
                        status=status.HTTP_404_NOT_FOUND)


"""
All url mappings are specified here to have a one-stop overview of what URLs
link to what views.
"""


webapp_urls = [
    path("", AppView.as_view())
]

device_urls = [
    path("discover", HumeDiscoverDevices.as_view()),
    path("<str:address>/attach", HumeAttachDevice.as_view()),
    path("<str:device_uuid>/action", DeviceAction.as_view()),
    path("<str:device_uuid>/change-room", ChangeDeviceRoom.as_view()),
]

hume_urls = [
    path("<str:hume_uuid>/devices/", include(device_urls)),
]

room_urls = [
    path("<int:room_id>/devices", RoomDevices.as_view()),
]

home_urls = [
    path("<int:home_id>/humes", HomeHumes.as_view()),
    path("<int:home_id>/humes/", include(hume_urls)),

    path("<int:home_id>/devices", HomeDevices.as_view()),

    path("<int:home_id>/rooms", HomeRooms.as_view()),
    path("<int:home_id>/rooms/", include(room_urls)),
]

api_urlpatterns = [
    #
    # HOMES
    #
    path("homes", Homes.as_view()),
    path("homes/", include(home_urls)),

    #
    # HUMES
    #
    path("humes", Humes.as_view()),  # not AJAX
    path("humes/broker-credentials", BrokerCredentials.as_view()),  # not AJAX
    # DO NOT PUT THIS URL ABOVE /broker-credentials :-)
    path("humes/<str:hume_uuid>", HumeFind.as_view()),
    path("humes/<str:hume_uuid>/devices", Devices.as_view()),  # not AJAX
    path("humes/<str:hume_uuid>/confirm-pairing",
         HumeConfirmPairing.as_view()),

    #
    # USERS
    #
    path("users/signup", UserSignup.as_view()),
    path("users/login", login_user),
    path("users/logout", logout_user),
    path("users/self", UserSelf.as_view()),

    # 404!
    path("", api_path_not_found),
    path("<path:url>", api_path_not_found)
]

urlpatterns = [
    path("api/", include(api_urlpatterns)),
    path("admin/", admin.site.urls),

    # Empty path will forward to front end Angular application.
    path("", include(webapp_urls)),
    # Catch all is forwarded to the Angular front end application, event 404's
    # are handled by the Angular application.
    path("<path:url>", include(webapp_urls)),
]
