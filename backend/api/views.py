from django.http import HttpResponse
from django.utils.decorators import decorator_from_middleware

from .request_handling import validate_request_fields
from .middleware import RequestFieldMiddleware


@decorator_from_middleware(RequestFieldMiddleware)
def heartbeat(request, request_fields=None):
    """Call both device and HUME procedure modules to handle the information"""
    print(request_fields)

    return HttpResponse(status=200)


# TODO: define the API structure returned by an Info Request!
@decorator_from_middleware(RequestFieldMiddleware)
def info(request, request_fields=None):
    """
    This will be an attempt at an API information source, what paths
    there are to query and so on.
    """

    # Expect the request to be empty, since GET
    valid = validate_request_fields(request_fields=request_fields)

    if valid:
        return HttpResponse()
    else:
        return HttpResponse(status=400)  # Bad request
