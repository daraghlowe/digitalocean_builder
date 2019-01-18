from django.conf.urls import url

from apps.digitalocean_builder.views import StatusView

urlpatterns = [
    # TODO: Should the status endpoint/view be defined in its own app or globally or here?
    url(r'^v1/status/?$', StatusView.as_view()),
]
