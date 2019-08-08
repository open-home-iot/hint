from backend.util.json_handling import extract_request_fields


class RequestFieldMiddleware:

    def process_view(self, request, view_func, view_args, view_kwargs):
        view_kwargs['request_fields'] = extract_request_fields(request)

        return None
