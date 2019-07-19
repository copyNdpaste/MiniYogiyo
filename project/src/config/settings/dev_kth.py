import json
from .base import *
from .utils import get_env_var

DEBUG = True

INSTALLED_APPS += [
    'django_extensions'
]

MIDDLEWARE += [
    'querycount.middleware.QueryCountMiddleware'
]

INTERNAL_IPS = ('127.0.0.1',)


SECRET_KEY = get_env_var("SECRET_KEY")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_var("NAME"),
        'USER': get_env_var("USER"),
        'PASSWORD': get_env_var("PASSWORD"),
        'HOST': get_env_var("HOST"),
        'PORT': get_env_var("PORT"),
    }
}

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]

#불필요시 주석처리
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}

QUERYCOUNT = {
    'THRESHOLDS': {
        'MEDIUM': 50,
        'HIGH': 200,
        'MIN_TIME_TO_LOG': 0,
        'MIN_QUERY_COUNT_TO_LOG': 0
    },
    'IGNORE_REQUEST_PATTERNS': [],
    'IGNORE_SQL_PATTERNS': [],
    'DISPLAY_DUPLICATES': None,
    'RESPONSE_HEADER': 'X-DjangoQueryCount-Count'
}
