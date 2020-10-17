from django.urls import path, include

from backend.user.views import login_user, logout_user, Users, UserSelf
from backend.home.views import Homes
from backend.hume.views import HumePair, HumeFind, HumeAssociate


user_patterns = [
    path("", Users.as_view()),
    path("login", login_user),
    path("logout", logout_user),
    path("self", UserSelf.as_view())
]

home_patterns = [
    path("", Homes.as_view()),
    # This is just to make it more readable and a more logical API, request ALL
    # HUMEs for a given home: /api/home/humes. Otherwise it will be cumbersome
    # to query for. Should create similar API view for devices of a given HUME.
    # Still, the view needs to enforce strict user checks to make sure some
    # other user is not querying for another user's HUMEs.
#    path("<id:int>/humes", HomeHumes.as_view())
]

hume_patterns = [
    path("pair", HumePair.as_view()),
    path("find", HumeFind.as_view()),
    path("<int:hume_id>/associate", HumeAssociate.as_view())
]

device_patterns = []

urlpatterns = [
    path("home/", include(home_patterns)),
    path("hume/", include(hume_patterns)),
    path("device/", include(device_patterns)),
    path("user/", include(user_patterns)),
]
