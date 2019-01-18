from django.conf.urls import url

from apps.metrics.views import MetricsView

urlpatterns = [
    url(r'^metrics/?$', MetricsView.as_view()),
]
