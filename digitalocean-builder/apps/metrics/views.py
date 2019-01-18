from rest_framework import renderers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from prometheus_client import exposition, CollectorRegistry

from apps.metrics.core import DatabaseCollector


class PlainTextRenderer(renderers.BaseRenderer):
    """
    This comes from the django rest framework documentation. Not sure why they don't just provide it with the other
    out of the box renderers (like JsonRenderer).
    """
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        return data.encode(self.charset)


class MetricsView(APIView):
    """
    return text/plain prometheus metrics
    """
    renderer_classes = (PlainTextRenderer,)
    permission_classes = (AllowAny,)

    def __init__(self):
        super().__init__()
        self.registry = CollectorRegistry()

        self.registry.register(
            # Add your collectors here. They should be of DatabaseCollector and contain a name, docstring, and a lambda
            # which when executed will execute a DB query. Replace mock_db_query below with your own query!
            DatabaseCollector(
                name='binary_gauge',
                documentation='An example gauge that returns 1 or 0 depending on the supplied argument',
                value=lambda: mock_db_query(True)
            )
        )

    def get(self, request):
        output = exposition.generate_latest(self.registry)
        return Response(output.decode("utf-8"), status=200)


def mock_db_query(argument: bool) -> int:
    """
    returns 0 or 1, depending on if argument is True or False. replace this with your DB query!
    example:
        from apps.dns.models import RecordAgentStatus
        return RecordAgentStatus.objects.filter(state=state).count()
    """
    if argument:
        return 1
    else:
        return 0
