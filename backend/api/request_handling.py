from importlib import import_module

from django.http import HttpResponse

from util.json_handling import extract_request_fields

from .views import heartbeat


def handle_incoming_request(request, path=None):
    request_fields = extract_request_fields(request)

    if not request_fields:
        return HttpResponse(status=400)
    else:
        return resolve_url(request, request_fields, path)


def resolve_url(request, request_fields, path):
    # Every path has two components
    (main, sub,) = path

    # Procedure to call
    procedure = None

    if main == 'heartbeat':
        procedure = heartbeat
    else:
        # Import the views of the procedure module
        module = import_module(main + '.views')
        procedure = getattr(module, sub)

    return procedure(request, request_fields)
