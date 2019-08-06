from django.http import HttpResponse
from django.utils.decorators import decorator_from_middleware

from backend.api_external.middleware import RequestFieldMiddleware


@decorator_from_middleware(RequestFieldMiddleware)
def event(request, request_fields=None):
    """A device event is received."""
    print(request_fields)

    return HttpResponse(status=200)
