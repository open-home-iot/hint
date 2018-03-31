from django.conf.urls import url

from rest_framework import routers

from api import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'info', views.InfoViewSet)


urlpatterns = [
    url(r'csrf', views.get_csrf_token),

    url(r'login', views.login_user),
    url(r'logout', views.logout_user),

    url(r'^events/', ([
        url(r'^alarm/(?P<alarm>\w+)$', views.event_alarm),
        url(r'^status$', views.get_event_status),
    ], 'events', 'alarms')),

    url(r'^surveillance/', ([
        url(r'^pictures$', views.list_pictures),
    ], 'surveillance', 'survey')),
] + router.urls
