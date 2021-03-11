from django.urls import path, include

from django.contrib import admin
from django.http import JsonResponse
from rest_framework import status

from backend.user.urls import urlpatterns as user_urls
from backend.home.urls import home_urls, room_urls
from backend.hume.urls import urlpatterns as hume_urls
from backend.device.urls import urlpatterns as device_urls

from backend.webapp.urls import urlpatterns as app_urls


# Put this here since it does not belong to any specific app's views
def api_path_not_found(request, url=None):
    """
    Returns a base 404 message and status for all API calls that lead nowhere.
    :param request:
    :param url: URL that had no match
    :return:
    """
    print(f"API URL: {url} does not exist!")
    return JsonResponse({"error": "Resource not found."},
                        status=status.HTTP_404_NOT_FOUND)


api_urlpatterns = [
    path("homes/", include(home_urls)),
    path("rooms/", include(room_urls)),
    path("humes/", include(hume_urls)),
    path("devices/", include(device_urls)),
    path("users/", include(user_urls)),

    # Catch non-supported URLs
    path("", api_path_not_found),
    path("<path:url>", api_path_not_found)
]

urlpatterns = [
    path("api/", include(api_urlpatterns)),
    path("admin/", admin.site.urls),

    # Empty path will forward to front end Angular application.
    path("", include(app_urls)),
    # Catch all is forwarded to the Angular front end application, event 404's
    # are handled by the Angular application.
    path("<path:url>", include(app_urls)),
]
