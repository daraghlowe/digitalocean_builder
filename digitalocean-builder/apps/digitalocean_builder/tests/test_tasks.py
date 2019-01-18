from django.test import TestCase

from ..tasks import celery_heartbeat


class TestTasks(TestCase):
    def test_celery_heartbeat(self):
        """
        Testing the successful_celery_task function
        """
        result = celery_heartbeat()
        self.assertDictEqual({'task': 'digitalocean_builder.celery_heartbeat'}, result)
