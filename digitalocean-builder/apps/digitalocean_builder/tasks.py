import logging

from config.celery import APP

LOGGER = logging.getLogger(__name__)


@APP.task(name='digitalocean_builder.celery_heartbeat')
def celery_heartbeat():
    """
    This task does nothing. We run it for the side-effect that a task completion
    will be recorded in django_celery_results.models.TaskResult, which we
    can then check in our status endpoint to make sure Celery is running.
    """

    LOGGER.info("Celery heartbeat!")
    return {'task': 'digitalocean_builder.celery_heartbeat'}
