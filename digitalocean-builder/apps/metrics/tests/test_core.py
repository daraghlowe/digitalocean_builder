from unittest import TestCase

from apps.metrics.core import DatabaseCollector
from apps.metrics.views import mock_db_query


class MetricsTest(TestCase):
    def test_database_gauge(self):
        database_collector = DatabaseCollector(
            name="test_gauge",
            documentation="a test gauge",
            value=lambda: mock_db_query(True),
        )
        metrics = list(database_collector.collect())
        self.assertEqual(1, len(metrics))

        samples = metrics[0].samples
        self.assertEqual(1, len(samples))

        sample = samples[0]
        self.assertEqual('test_gauge', sample.name)
        self.assertTrue(sample.value)
