from django.urls import path, include

from django.contrib import admin

from backend.user.urls import urlpatterns as user_urls
from backend.home.urls import urlpatterns as home_urls
from backend.hume.urls import urlpatterns as hume_urls
from backend.device.urls import urlpatterns as device_urls

from backend.webapp.urls import urlpatterns as app_urls


ajax_urlpatterns = [
    path("home/", include(home_urls)),
    path("hume/", include(hume_urls)),
    path("device/", include(device_urls)),
    path("user/", include(user_urls)),
]

urlpatterns = [
    path("api/", include(ajax_urlpatterns)),
    path("admin/", admin.site.urls),

    # Empty path will forward to front end Angular application.
    path("", include(app_urls)),
    # Catch all is forwarded to the Angular front end application, event 404's
    # are handled by the Angular application.
    path("<path:url>", include(app_urls)),
]
