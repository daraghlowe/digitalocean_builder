from unittest.mock import patch

from django.test import TestCase


class MetricsEndpointTest(TestCase):

    @patch('apps.metrics.views.mock_db_query')
    def setUp(self, mock_db_query):
        mock_db_query.return_value = 1
        response = self.client.get('/metrics')
        self.assertEqual(200, response.status_code)
        self.lines = list(response.content.decode("utf-8").splitlines())

    def test_binary_gauge(self):
        self.assertIn("# HELP binary_gauge An example gauge that returns 1 or 0 depending on the supplied argument",
                      self.lines)
        self.assertIn("# TYPE binary_gauge gauge", self.lines)
        self.assertIn("binary_gauge 1.0", self.lines)
