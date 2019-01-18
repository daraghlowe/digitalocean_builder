"""
TODO Fill me in about what this module does, and why does it have a relative and * import?
"""

import os

from .base import *

SECRET_KEY = os.environ['DJANGO_SECRET_KEY'] # raises KeyError when misconfigured

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 1

# Logging
# https://docs.djangoproject.com/en/1.11/topics/logging/
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'json': {
            '()': 'wpe_django_logging.formatters.StackDriverJSONFormatter',
            'fmt': '%(levelname)s %(asctime)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'json'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'apps': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
dictConfig(LOGGING)

PROMETHEUS_METRICS_EXPORT_PORT_RANGE = range(7000, 7004)
