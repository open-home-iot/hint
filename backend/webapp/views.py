import subprocess

from django.views.generic.base import TemplateView
from django.http import JsonResponse
from django.conf import settings

from rest_framework import status


class AppView(TemplateView):
    template_name = "index.html"


def revision(request):
    """
    Return the revision of HINT currently in use.
    """
    commit_id = subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"]
    ).decode() if settings.DEBUG and not settings.BUILD else settings.COMMIT_ID
    tag = subprocess.check_output(
        ["git", "describe", "--tags"]
    ).decode() if settings.DEBUG and not settings.BUILD else settings.SEMVER
    return JsonResponse({"commit_id": commit_id, "tag": tag},
                        status=status.HTTP_200_OK)
