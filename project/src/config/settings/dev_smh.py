import json
from .base import *
from .utils import get_env_var

DEBUG = True

INSTALLED_APPS += [
    'coverage',
    'debug_toolbar',
    'django_extensions',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS=('127.0.0.1',)


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
