import subprocess

from django.views.generic.base import TemplateView
from django.http import JsonResponse

from rest_framework import status


class AppView(TemplateView):
    template_name = "index.html"


REVISION = subprocess.check_output(
    ["git", "rev-parse", "--short", "HEAD"]
).decode()
TAG = subprocess.check_output(
    ["git", "describe", "--tags"]
).decode()


def revision(request):
    """
    Return the revision of HINT currently in use.
    TODO: add git tag once in use
    """
    return JsonResponse({"commit_id": REVISION, "tag": TAG},
                        status=status.HTTP_200_OK)
