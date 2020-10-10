from django.urls import path, include

from backend.user.views import login_user, logout_user, Users, UserSelf
from backend.home.views import CreateHome, UpdateHome, ListHome


home_patterns = [
    path("create", CreateHome.as_view()),
    path("update", UpdateHome.as_view()),
    path("list", ListHome.as_view()),
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
