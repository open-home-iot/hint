from django.urls import path

from backend.user.views import login_user, logout_user, Users, UserSelf


urlpatterns = [
    path("signup", Users.as_view()),
    path("login", login_user),
    path("logout", logout_user),
    path("self", UserSelf.as_view())
]
