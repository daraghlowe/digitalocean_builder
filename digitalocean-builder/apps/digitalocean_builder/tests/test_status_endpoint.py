from typing import Optional
from unittest.mock import patch

from django.conf import settings
from django.db.models.query import QuerySet
from django.test import TestCase
from wpe_django_auth.auth_mock import get_auth_header
from wpe_django_swagger.swagger_testing import SwaggerContractClient


@patch('apps.digitalocean_builder.views.APP', autospec=True)
class StatusEndpointTest(TestCase):
    STATUS_ENDPOINT = '/v1/status'

    def setUp(self):
        self.client = SwaggerContractClient(HTTP_ACCEPT='application/json')
        self.auth_headers = get_auth_header()

    def test_success_unauthenticated(self, mock_app):
        response = self.get({'pretty': True})

        self.assert_success(response)
        self.assertNotIn('services', response.json().keys())

    def test_success_authenticated(self, mock_app):
        response = self.authenticated_get({'pretty': True})

        self.assertEqual(200, response.status_code)
        self.assertTrue(response.json()['services']['database']['success'])

    def test_expected_services(self, mock_app):
        expected_service_names = {"database", "celery"}
        response = self.authenticated_get()
        services = response.json()['services']
        service_names = set(services.keys())

        self.assertEqual(
            expected_service_names, service_names,
            "We expect to run 2 services: database & celery"
        )

    def test_expected_services_no_celery(self, mock_app):
        """
        When celery isn't configured, its status should not be checked/returned.
        """
        # When:
        url_setting = 'django.conf.settings.CELERY_BROKER_URL'
        with patch(url_setting, new_callable=none_factory):
            response = self.authenticated_get()

        # Then:
        expected_service_names = {"database"}
        services = response.json()['services']
        service_names = set(services.keys())

        self.assertEqual(
            expected_service_names, service_names,
            "Only the 'database' service should be checked/returned."
        )

    @patch.object(QuerySet, 'count')
    def test_failure_generic_exception(self, mock_count, mock_app):
        mock_count.side_effect = Exception('Test generic exception!')
        response = self.client.get(self.STATUS_ENDPOINT)
        self.assertEqual(response.status_code, 200)

    def assert_success(self, response):
        """Assert that our status endpoint returned success."""

        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.json()["success"])

    def test_version_in_status(self, mock_app):
        response = self.get({'pretty': True})

        self.assert_success(response)
        data = response.json()
        self.assertIn('version', data)
        self.assertEqual(settings.VERSION, data['version'])

    def test_git_sha_in_status(self, mock_app):
        response = self.get({'pretty': True})

        self.assert_success(response)
        data = response.json()
        self.assertIn('git_sha', data)
        self.assertEqual(settings.GIT_COMMIT, data['git_sha'])

    def get(self, params: Optional[dict] = None, *, headers: Optional[dict] = None):
        """Make an HTTP GET on the status endpoint."""
        if not params:
            params = {}
        if not headers:
            headers = {}

        return self.client.get(self.STATUS_ENDPOINT, params, **headers)

    def authenticated_get(self, params: Optional[dict] = None, *, headers: Optional[dict] = None):
        send_headers = {}
        if headers:
            send_headers.update(headers)
        send_headers.update(self.auth_headers)

        return self.get(params=params, headers=send_headers)


def none_factory():
    """Returns an (the) instance of None."""
    return None
