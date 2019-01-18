# Monitoring

## New Relic

digitalocean-builder reports data to new relic for both the staging and production instances. All of our corporate
applications can be found on this [New Relic List](https://rpm.newrelic.com/accounts/1048778/applications).

## Prometheus

digitalocean-builder includes the django-prometheus middleware to expose a default set of prometheus metrics, and
allows you to expose application specific metrics as well.  The production deployment includes an example of creating
an application specific Prometheus alert for 50X errors, which can be extended to include alerts for your custom metrics.
