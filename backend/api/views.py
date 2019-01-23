from django.http import HttpResponse, JsonResponse

from .request_validation import validate_request_fields


def heartbeat(request, request_fields):
    """Call both device and HUME procedure modules to handle the information"""

    return HttpResponse(status=200)


def info(request, request_fields=None):
    """This will be an attempt at an API information source, what paths
       there are to query and so on."""

    # Expect the request to be empty, since GET
    valid = validate_request_fields(request_fields=request_fields)

    if valid:
        return HttpResponse()
    else:
        return HttpResponse(status=400)  # Bad request
