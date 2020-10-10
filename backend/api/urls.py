from django.urls import path, include

from backend.user.views import login_user, logout_user, Users, UserSelf
from backend.home.views import Homes


home_patterns = [
    path("", Homes.as_view()),
]

hume_patterns = []

device_patterns = []

user_patterns = [
    path("", Users.as_view()),
    path("login", login_user),
    path("logout", logout_user),
    path("self", UserSelf.as_view())
]

urlpatterns = [
    path("home/", include(home_patterns)),
    path("hume/", include(hume_patterns)),
    path("device/", include(device_patterns)),
    path("user/", include(user_patterns)),
]
