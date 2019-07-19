"""
Django settings for config project.
"""

import os

from django.urls import reverse_lazy

from .utils import get_env_var

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'home',
    'accounts',
    'category',
    'restaurant',
    'yosigy',
    # th
    'cart',
    'order',
    'background_task',

    # mh
    'menu',
    'grid',
    'timeline',
    'grouppurchase',

    # sr
    'coupon',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'accounts.pipeline.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.user.user_details',
)

SOCIAL_AUTH_POSTGRES_JSONFIELD = True

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = get_env_var('GOOGLE_KEY')

SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = get_env_var('GOOGLE_SECRET')

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email']

AUTH_USER_MODEL = 'accounts.User'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = reverse_lazy('home')

LOGIN_REDIRECT_URL = reverse_lazy('home')

LOGIN_URL = reverse_lazy('home')

NEW_USER_REDIRECT_URL = reverse_lazy('accounts:my_page')
# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EXPIRATION_PERIOD = 90

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'test190508@gmail.com'
EMAIL_HOST_PASSWORD = get_env_var('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_MAIL = 'mini_admin'

ONE_RANDOM_MENU_COUNT = 1
DEFAULT_SCORE = 5
TOP_FIVE = 5
TOP_SCORE = 10

RANDOM_SCORE_WEIGHT = 1
HIT_SCORE_WEIGHT = 1.5
LIKE_SCORE_WEIGHT = 2.5
ORDER_SCORE_WEIGHT = 2.5
RECOMMENDED_SCORE_WEIGHT = 2.5

BACKGROUND_TASK_RUN_ASYNC = True
LOCALHOST = 'http://127.0.0.1:8000'

POPULAR_MENU_LIST_MAX_LENGTH = 10
