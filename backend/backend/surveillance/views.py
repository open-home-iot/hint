from os import listdir, getenv, path

from django.http import JsonResponse


def list_pictures(req):
    user = getenv('DJANGO_STATIC_DIR', '~/')
    if user == '~/':
        raise EnvironmentError('You do not seem to have installed the project correctly, environment variable missing.')

    p = path.expanduser(user) + '/alarm_pictures/'

    result = listdir(p)

    return JsonResponse({'pictures': result})
