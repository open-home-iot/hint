from django.urls import path

from backend.user.views import login_user, logout_user, UserSignup, UserSelf


urlpatterns = [
    #Using the class UserSignup as a view
    path("signup", UserSignup.as_view()),
    path("login", login_user),
    path("logout", logout_user),
    path("self", UserSelf.as_view())
]
