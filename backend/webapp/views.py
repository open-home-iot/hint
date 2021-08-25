import subprocess

from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.conf import settings

from rest_framework import status


class AppView(TemplateView):
    template_name = "index.html"


COMMIT_ID = subprocess.check_output(
    ["git", "rev-parse", "--short", "HEAD"]
).decode() if not settings.BUILD else "cid"
TAG = subprocess.check_output(
    ["git", "describe", "--tags"]
).decode() if not settings.BUILD else "tag"


def revision(request):
    """
    Return the revision of HINT currently in use.
    TODO: add git tag once in use
    """
    return JsonResponse({"commit_id": COMMIT_ID, "tag": TAG},
                        status=status.HTTP_200_OK)
