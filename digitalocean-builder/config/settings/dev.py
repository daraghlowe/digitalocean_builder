"""
TODO Fill me in about what this module does, and why does it have a relative and * import?
"""

from .base import *

DEBUG = True
SECRET_KEY = 'garbage'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

EMAIL_BACKEND = 'django.mail.backends.console.EmailBackend'

WPE_AUTH_URL    = 'https://auth-staging.wpengine.io/v1/tokens/'
