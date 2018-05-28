from django.urls import path, include

from rest_framework import routers

from api import views

# Note that it is important as of now to append a final slash to each URL!

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'info', views.InfoViewSet)
router.register(r'alarm_history', views.AlarmHistoryViewSet, base_name='alarm_history')
router.register(r'surveillance_configuration', views.SurvConfigurationViewSet)

urlpatterns = [
    path('csrf/', views.get_csrf_token),

    path('login/', views.login_user),
    path('logout/', views.logout_user),

    path('surveillance_pictures/', views.PictureViewSet.as_view()),
    path('alarm_status/', views.alarm_status)
] + router.urls
