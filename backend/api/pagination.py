from rest_framework.views import api_settings


class PaginationMixin:

    def paginate_response(self, results, request):
        [pagination_class, ] = api_settings.DEFAULT_PAGINATION_CLASS
        paginator = pagination_class()
        page = paginator.paginate_queryset(results, request)

        return paginator.get_paginated_response(page)
