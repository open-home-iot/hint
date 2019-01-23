from util.json_handling import extract_request_fields


class RequestFieldMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        view_kwargs['request_fields'] = extract_request_fields(request)

        return None
