"""
Smoke tests to be run after each deploy.
"""

import os
import requests

from retry import retry
from unittest import TestCase
from parameterized import parameterized


class digitaloceanBuilderApp:

    @property
    def base_url(self):
        return 'https://{}'.format(os.environ.get('SMOKE_DOMAIN', default='digitalocean-builder.wpesvc.net'))

    @property
    def status_url(self):
        return '{}/v1/status/'.format(self.base_url)

    @property
    def version(self):
        return os.environ.get('VERSION')

    @property
    def git_sha(self):
        return os.environ.get('GIT_COMMIT')


# Parameterizing the SMOKE_DOMAIN so a unique function name is created for the test results in case there are
# smoke tests for both staging and production.
# If we don't create a unique name, test results for staging and production will appear as duplicates in jenkins.
class StatusTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = digitaloceanBuilderApp()
        cls.response = requests.get(cls.app.status_url)
        cls.json_response = cls.response.json()

    @parameterized.expand([os.environ.get('SMOKE_DOMAIN', default='digitalocean-builder.wpesvc.net')])
    def test_status_ok(self, name):
        @retry("Wait for the deploy to finish.")
        def block():
            self.assertEqual(200, self.response.status_code, 'Expected 200 status code:  {}'.format(self.response.text))
            self.assertTrue(self.json_response['success'], 'Status check failed:  {}'.format(self.response.text))

    @parameterized.expand([os.environ.get('SMOKE_DOMAIN', default='digitalocean-builder.wpesvc.net')])
    def test_version_number(self, name):
        @retry("Wait for the deploy to finish.")
        def block():
            self.assertIn('version', self.json_response, 'Version not found in status: {}'.format(self.response.text))
            self.assertEqual(self.app.version, self.json_response['version'], 'Expected version {}:  {}'.format(
                self.app.version, self.json_response['version']))

    @parameterized.expand([os.environ.get('SMOKE_DOMAIN', default='digitalocean-builder.wpesvc.net')])
    def test_git_sha(self, name):
        @retry("Wait for the deploy to finish.")
        def block():
            self.assertIn('git_sha', self.json_response, 'Git SHA not found in status: {}'.format(self.response.text))
            self.assertEqual(self.app.git_sha, self.json_response['git_sha'], 'Expected Git SHA {}:  {}'.format(
                self.app.git_sha, self.json_response['git_sha']))
