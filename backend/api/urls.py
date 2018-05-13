from django.urls import path, include

from rest_framework import routers

from api import views

# Note that it is important as of now to append a final slash to each URL!

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'info', views.InfoViewSet)

surveillance_urlpatterns = [
    path('pictures/', views.PictureList.as_view()),
]

event_urlpatterns = [
    path('alarm/<str:alarm>', views.event_alarm),
    path('status/', views.get_event_status)
]

urlpatterns = [
    path('csrf/', views.get_csrf_token),

    path('login/', views.login_user),
    path('logout/', views.logout_user),

    path('surveillance/', include(surveillance_urlpatterns)),

    path('events/', include(event_urlpatterns)),
] + router.urls
