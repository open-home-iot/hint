import requests

from django.conf import settings


class HttpRequest:
    POST = 1
    GET = 2

    def __init__(self, method, target, **kwargs):
        self.method = method
        self.target = HttpRequest.create_target_address(target)
        self.payload = kwargs.get('payload', {})

    @classmethod
    def create_target_address(cls, target):
        (ip, extension,) = target
        return settings.HUME_PREFFERED_PROTOCOL + ip + \
            settings.HUME_PREFFERED_PORT + extension

    def send(self):
        if self.method == HttpRequest.POST:
            return self.post()
        else:
            return self.get()

    def post(self):
        return requests.post(self.target, json=self.payload)

    def get(self):
        return requests.get(self.target)


def validate_request_fields(required_fields=[],
                            optional_fields=[],
                            request_fields={}):
    """DO NOT MANIPULATE request_fields!"""

    keys = list(request_fields.keys())

    try:
        for key in required_fields:
            keys.remove(key)
    except ValueError:
        return False

    # Pop all optional fields and ensure no leftover trash is left in
    # request_fields
    for key in optional_fields:
        try:
            keys.remove(key, None)  # Ignore exception this time, we only want
                                    # to clear it
        except ValueError:
            pass

    return len(keys) == 0
