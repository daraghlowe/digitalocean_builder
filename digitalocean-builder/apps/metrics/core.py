"""
Types for collecting and exporting prometheus metrics. Named core to be consistent with prometheus_client.
"""
from prometheus_client.core import GaugeMetricFamily


class DatabaseCollector:
    """
    Provide a name, docstring, and a function which when called will make a query to the db to retrieve a count. This
    collector should be used in your views to provide metrics that query the database.
    TODO: this metrics module should be moved to a library: https://wpengine.atlassian.net/browse/T2-374
    """

    def __init__(self, name, documentation, value):
        self.name = name
        self.documentation = documentation
        self.value = value

    # See this for details:  https://github.com/prometheus/client_python#custom-collectors
    def collect(self):
        yield GaugeMetricFamily(self.name, self.documentation, value=self.value())
