from django.http import HttpResponse

from util.json_handling import extract_request_fields


def handle_incoming_request(request):
    request_fields = extract_request_fields(request)

    print("checking request fields...")

    if not request_fields:
        stop()
    else:
        resolve_url(request, request_fields)


def stop():
    return HttpResponse(status=400)


def resolve_url(request, request_fields):
    url_path_parts = request.path.split('/')
    print(url_path_parts)

    return HttpResponse(status=400)
