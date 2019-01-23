import requests

from importlib import import_module

from django.http import HttpResponse

from util.json_handling import extract_request_fields

from .views import heartbeat


def handle_incoming_request(request, path=None):

    def resolve_url(request, request_fields, path):
        # Every path has two components
        (main, sub,) = path

        # Procedure to call
        procedure = None

        if sub == '':
            module = import_module('.views', package='api')
            procedure = getattr(module, main)
        else:
            # Import the views of the procedure module
            module = import_module(main + '.views')
            procedure = getattr(module, sub)

        return procedure(request, request_fields)

    request_fields = extract_request_fields(request)

    return resolve_url(request, request_fields, path)


class HttpRequest():

    def __init__(self, *args, **kwargs):
        pass
