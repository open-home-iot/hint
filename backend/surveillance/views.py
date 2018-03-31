import os

from django.http import JsonResponse


def list_pictures(req):
    user = os.getenv('DJANGO_STATIC_DIR', '~/')
    if user == '~/':
        raise EnvironmentError('You do not seem to have installed the project correctly, environment variable missing.')

    p = os.path.expanduser(user) + '/alarm_pictures/'

    result = os.listdir(p)

    return JsonResponse({'pictures': result})
