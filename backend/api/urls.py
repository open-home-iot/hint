from django.urls import path, include

from backend.user.views import login_user, logout_user, CreateUser


hume_patterns = []

device_patterns = []

user_patterns = [
    path("login", login_user),
    path("logout", logout_user),
    path("sign-up", CreateUser.as_view())
]

urlpatterns = [
    path("hume/", include(hume_patterns)),
    path("device/", include(device_patterns)),
    path("user/", include(user_patterns)),
]
