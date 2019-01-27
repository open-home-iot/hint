import json

from json.decoder import JSONDecodeError


def extract_request_fields(request):
    decoded_data = {}

    try:
        decoded_data = json.loads(request.body)
    except JSONDecodeError:
        pass

    if isinstance(decoded_data, dict):
        return decoded_data
    else:
        return {}


def pack_request_fields(payload):
    return json.dumps(payload)
