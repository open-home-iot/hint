from django.http import HttpResponse
from django.db.models import Q
from django.utils.decorators import decorator_from_middleware

from .models import Hume

from api.request_handling import validate_request_fields
from api.middleware import RequestFieldMiddleware


@decorator_from_middleware(RequestFieldMiddleware)
def attach(request, request_fields=None):
    required_fields = ('hume_id',)

    valid = validate_request_fields(required_fields=required_fields,
                                    request_fields=request_fields)

    status_code = 400

    if valid:
        ip_address = request.META.get('REMOTE_ADDR')
        hume_id = request_fields.get('hume_id')

        if Hume.objects.filter(Q(id=hume_id) | Q(ip_address=ip_address)).exists():
            status_code = 409  # Conflict
        else:
            Hume.objects.create(id=hume_id, ip_address=ip_address)
            status_code = 200

    else:
        pass

    return HttpResponse(status=status_code)


@decorator_from_middleware(RequestFieldMiddleware)
def authentication(request, request_fields=None):
    return HttpResponse(status=200)


@decorator_from_middleware(RequestFieldMiddleware)
def token_update(request, request_fields=None):
    return HttpResponse(status=200)
