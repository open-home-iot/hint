import os

from .base import *  # noqa

DEBUG = False
BUILD = False
SECRET_KEY = os.environ["SECRET_KEY"]

HUME_BROKER_USERNAME = os.environ["BROKER_USER"]
HUME_BROKER_PASSWORD = os.environ["BROKER_PASS"]

HUME_BROKER_HOST = os.environ["BROKER_HOST"]
HUME_BROKER_PORT = int(os.environ["BROKER_PORT"])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hint',
        'USER': os.environ["PG_USER"],
        'PASSWORD': os.environ["PG_PASS"],
        'HOST': os.environ["PG_HOST"],
        'PORT': os.environ["PG_PORT"]
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                (os.environ["REDIS_HOST"], int(os.environ["REDIS_PORT"]))
            ],
            # Seconds until a channel is removed from a group
            "group_expiry": 600,
        },
    },
}
