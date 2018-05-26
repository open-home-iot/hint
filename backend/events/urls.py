from django.urls import path

from events import views


urlpatterns = [
    path('alarm/off/', views.alarm_off),
    path('alarm/on/<str:date>/', views.alarm_on),
]
