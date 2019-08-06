from __future__ import absolute_import, unicode_literals
from celery import shared_task

from backend.api_external.request_handling import HttpRequest
from .models import Hume


"""
This module will be automatically picked up by Celery as a task defining
module, due to its name 'tasks.py'.
"""


def identification_request(hume_id, username, password):
    identification_request_async.delay(hume_id, username, password)


@shared_task
def identification_request_async(hume_id, username, password):
    """
    POST a request to the target HUME with its associated login credentials.
    """
    EXTENSION = '/hume/identification'

    hume = Hume.objects.get(id=hume_id)

    payload = {
        'hume_username': username,
        'hume_password': password
    }

    request = HttpRequest(HttpRequest.POST,
                          (hume.ip_address, EXTENSION,),
                          payload=payload)
    response = request.send()

    # TODO notify frontend
    if response.status_code == 200:
        pass
    else:
        pass
