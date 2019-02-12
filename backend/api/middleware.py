from util.json_handling import extract_request_fields


class RequestFieldMiddleware:
    """
    To use the decorator decorator_from_middleware, we need to use the
    1.9 django style of middleware classes, excluding the __init__.
    __init__ in django 1.9 does not accept any arguments, while > 2 does
    expect get_response.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        view_kwargs['request_fields'] = extract_request_fields(request)

        return None
