from django.urls import path, include

from api import urls as api_urls


# Note that it is important as of now to append a final slash to each URL!
urlpatterns = [
    # Custom apps
    path('api/', include(api_urls)),
]
