import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

# Normally, the final os.path uses abspath(), we use dirname() here instead
# since we want the top level to be the root.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


# OPEN HOME SPECIFIC

HINT_BROKER_USERNAME = os.environ.get("HINT_BROKER_USER", "hint")
HINT_BROKER_PASSWORD = os.environ.get("HINT_BROKER_PASS", "hintpw123")
HUME_BROKER_USERNAME = os.environ.get("HUME_BROKER_USER", "hub")
HUME_BROKER_PASSWORD = os.environ.get("HUME_BROKER_PASS", "hubpw123")

BROKER_VHOST = os.environ.get("BROKER_VHOST", "hub")
BROKER_HOST = os.environ.get("BROKER_HOST", "127.0.0.1")
BROKER_PORT = int(os.environ.get("BROKER_PORT", 5672))

MASTER_COMMAND_QUEUE_NAME = "hint_master"


# Version information

COMMIT_ID = "cid"
SEMVER = "semver"


# Security

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "$7&9-c0=r=*1=!bew*^1rfm)$eu-mrx=vn(7al+5)tk!bsks#q"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
BUILD = False

# There currently isn't a need to check the host header since 1 value is only
# ever possible.
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")
CSRF_TRUSTED_ORIGINS = os.environ.get(
    "CSRF_TRUSTED_ORIGINS", "http://*,https://*"
).split(",")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom
    'backend.core.apps.CoreConfig',
    'backend.broker.apps.BrokerConfig',
    'backend.user.apps.UserConfig',
    'backend.home.apps.HomeConfig',
    'backend.hume.apps.HumeConfig',
    'backend.device.apps.DeviceConfig',
    'backend.webapp.apps.WebappConfig',
    'backend.godmode.apps.GodmodeConfig',

    # Third party
    'channels',
    'rest_framework'
]

MIDDLEWARE = [
    # Django MIDDLEWARE
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'backend/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Channels settings

# With channels enabled, we are now running an ASGI application.
ASGI_APPLICATION = 'backend.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(os.environ.get("REDIS_HOST", "127.0.0.1"),
                       int(os.environ.get("REDIS_PORT", 6379)))],
            # Seconds until a channel is removed from a group
            "group_expiry": 600,
        },
    },
}


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = dict()
if bool(os.environ.get("DB_POSTGRES", False)):
    DATABASES["default"] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hint',
        'USER': os.environ["POSTGRES_USER"],
        'PASSWORD': os.environ["POSTGRES_PASS"],
        'HOST': os.environ["POSTGRES_HOST"],
        'PORT': os.environ["POSTGRES_PORT"]
    }
else:
    DATABASES["default"] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'hint.sqlite3',
    }


# Models

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Authentication

AUTH_USER_MODEL = 'user.User'


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]


# Django Rest Framework (DRF)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = f"{BASE_DIR}/backend/static/collectedstatic"
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "backend/static"),
]


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname:^8} {name} - {message}',
            'datefmt': '%d/%m/%Y %H:%M:%S',
            'style': '{'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'asyncio': {
            'propagate': False,
        },
        'django': {
            'level': 'INFO',
        },
        'rabbitmq_client': {
            'level': 'INFO',
        },
        'pika': {
            'propagate': False,
        },
        'daphne': {
            'level': 'INFO',
        },
        'aioredis': {
            'level': 'INFO',
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
