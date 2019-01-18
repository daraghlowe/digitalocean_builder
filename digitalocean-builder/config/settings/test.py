"""
TODO Fill me in about what this module does, and why does it have a relative and * import?
"""

from .base import *

SECRET_KEY = 'test-garbage'
CELERY_ALWAYS_EAGER = True

INSTALLED_APPS.append('django_nose')
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
    'wpe_django_auth.auth_mock.MockServiceAuthentication',
)

WPE_AUTH_USER   = 'serviceuser'
