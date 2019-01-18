"""
Django settings for digitalocean-builder project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from logging.config import dictConfig

import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/


# SECRET_KEY is intentionally not set here

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Since our app is running on port 3000, we're isolated from any external traffic, and our nginx container is handling
# all SSL termination, we don't need to redirect any HTTP traffic
SECURE_SSL_REDIRECT = False

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

ALLOWED_HOSTS = ['digitalocean-builder.wpesvc.net',
                 'digitalocean-builder-staging.wpesvc.net']

POD_IP = os.environ.get('POD_IP')
if POD_IP:
    ALLOWED_HOSTS.append(POD_IP)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
    'rest_framework',
    'wpe_django_swagger',
    'wpe_django_auth',
    'django_prometheus',
    'apps.digitalocean_builder',
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Logging
# https://docs.djangoproject.com/en/1.11/topics/logging/
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'full': {
            'format': '[%(levelname)s] - %(asctime)s - %(name)s - %(message)s',
            'datefmt': '%y %b %d, %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'full'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'apps': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'celery': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
dictConfig(LOGGING)

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {'default': dj_database_url.config(conn_max_age=600)}

# Celery configuration
def _celery_broker_url():
    # This is a function to let us use local variables w/o polluting the
    # global settings namespace:
    host = os.environ.get('REDIS_HOST')
    password = os.environ.get('REDIS_PASSWORD')
    if host and (password is not None):
        return f'redis://:{password}@{host}:6379'

    # No redis configuration was present. This is valid, for example, if we
    # aren't (yet) using Celery for this project. In that case, we don't run
    # a Redis instance:
    return None

CELERY_BROKER_URL = _celery_broker_url()

# Default to JSON only (no pickling)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_RESULT_BACKEND = 'django-db'

# Build INFO
VERSION = os.environ.get('VERSION', 'unknown')
GIT_COMMIT = os.environ.get('GIT_COMMIT', 'unknown')

REST_FRAMEWORK = {
    'PAGE_SIZE': 20,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'wpe_django_auth.auth.ServiceAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

WPE_AUTH_URL = 'https://auth.wpengine.io/v1/tokens/'

# user and secret must live in the backend (e.g. LDAP)
WPE_AUTH_USER = 'your username here'
WPE_AUTH_SECRET = 'your secret here'

# number of seconds to cache auth response (optional)
WPE_AUTH_CACHE_TIMEOUT = 3600

WPE_SWAGGER_FILE = '/digitalocean-builder/specification/swagger.yml'

rollbar_access_token = os.environ.get('ROLLBAR_ACCESS_TOKEN')

if rollbar_access_token:
    # This middleware should be added last
    MIDDLEWARE.extend(['rollbar.contrib.django.middleware.RollbarNotifierMiddleware'])

    ROLLBAR = {
        'access_token': rollbar_access_token,
        'environment': os.environ.get('ENVIRONMENT', 'unspecified'),
        'branch': 'master',
        'root': BASE_DIR,
        'scrub_fields': ['authorization'],
        'locals': {
            'safe_repr': False
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = False
USE_TZ = True

# Default date format should include the timezone
DATETIME_FORMAT = 'D N j, Y, P e'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = '/var/www/static/'
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

