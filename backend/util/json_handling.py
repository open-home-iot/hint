import json

from json.decoder import JSONDecodeError


def extract_request_fields(request):
    try:
        decoded_data = json.loads(request.body)
        return decoded_data
    except JSONDecodeError:
        return {}
