"""
TODO Fill me in about what this module does.
"""

import os

import rollbar
from celery import Celery
from celery.schedules import crontab
# set the default Django settings module for the 'celery' program.
from celery.signals import task_failure
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

APP = Celery('digitalocean-builder')
APP.config_from_object('django.conf:settings', namespace='CELERY')

APP.autodiscover_tasks()

# Set up scheduled tasks here
APP.conf.beat_schedule = {
    'celery-heartbeat': {
        'task': 'digitalocean_builder.celery_heartbeat',
        'schedule': crontab(minute='*')  # Every minute
    },
}


@task_failure.connect
def publish_failure_to_rollbar(sender, task_id, einfo, **kwargs):
    """
    TODO Fill me in with something informative.
    :param sender:
    :param task_id:
    :param einfo:
    :param kwargs:
    :return:
    """
    if settings.ROLLBAR['access_token']:
        rollbar.init(
            access_token=settings.ROLLBAR['access_token'],
            environment=settings.ROLLBAR['environment']
        )

        rollbar.report_exc_info(
            exc_info=einfo.exc_info,
            extra_data={
                'task': sender.name,
                'task_id': task_id,
                'args': kwargs['args'],
                'kwargs': kwargs['kwargs']
            }
        )
    else:
        print('Task Failure:')
        print(sender.name)
        print(task_id)
        print(kwargs)
