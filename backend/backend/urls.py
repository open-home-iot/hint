from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from api import urls as api_urls


# Note that it is important as of now to append a final slash to each URL!


urlpatterns = [
    # Custom apps
    path('api/', include(api_urls)),

    # Admin + rest api
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
