from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from config.celery import APP


# Create your views here.
class StatusView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        """
        An endpoint to return the current status/availability of digitalocean-builder.
        ---
        responseMessages:
            - code: 200
              message: digitalocean-builder is running, examine 'success' value for status of dependencies.
            - code: 500
              message: digitalocean-builder is hard down.
        """
        response = {
            'success': False,
            'created_on': timezone.now(),
            'version': settings.VERSION,
            'git_sha': settings.GIT_COMMIT
        }
        services = self.verify_all_services()

        # If user is authenticated, display which services are available
        if request.user.is_authenticated:
            response['authenticated'] = True
            response['services'] = services

        response['success'] = all(service['success'] for service in services.values())

        extra_params = {}
        if "pretty" in request.GET:
            extra_params = {
                "indent": 4,
                "sort_keys": True
            }

        return JsonResponse(response, json_dumps_params=extra_params)

    def verify_all_services(self):
        """
        Verify all services digitalocean-builder depends on
        """
        statuses = {
            'database': self.verify_database(),
            'celery': self.verify_celery()
        }

        # Filter out any Nones -- this may be returned by services functions
        # to indicate that their service is not present.
        statuses = {
            service_name: status
            for service_name, status in statuses.items()
            if status is not None
        }

        return statuses

    def verify_database(self):
        try:
            User.objects.count()
            return {'success': True}
        except Exception as error:
            return {
                'success': False,
                'error': str(error)
            }

    @staticmethod
    def verify_celery():
        if not settings.CELERY_BROKER_URL:
            # Celery is not configured to run with this server:
            return None

        return {'success':  APP.control.inspect().active() is not None}
