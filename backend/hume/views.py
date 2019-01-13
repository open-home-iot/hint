from django.http import HttpResponse

from json.decoder import JSONDecodeError
from util.json_handling import extract_request_fields

from .models import Hume


def attach(request):
    request_fields = extract_request_fields(request)

    return HttpResponse(status=200)
