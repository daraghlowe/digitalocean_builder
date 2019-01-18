# Deployment

digitalocean-builder is continuously deployed through Jenkins on merges to master. There are 2 primary tools we
use for deploying digitalocean-builder. [Helm] and [Terraform].

## DNS

DNS is automatically created for your deployment, using the `dnsName` value in your helm values files in the
`deploy/helm-values` directories.

## Terraform

Terraform manages the cloud resources digitalocean-builder uses. We have a separate stack for staging and
production and both live under deploy/terraform.

Changes to these stacks are applied through Jenkins during the regular CI/CD process.

## Helm

Helm manages the kubernetes pieces of our application (which containers to run, how to scale them, how to expose them
to the internet, etc.).  By default, the project is using a shared chart called
[django-api](https://github.com/wpengine/helm-charts/tree/master/stable/django-api).  The chart is managed separately
from the application because it is abstracted to be reused by multiple deployments.

## Secrets

### Vault

[Here](https://wpengine.atlassian.net/wiki/spaces/SYS/pages/265093133/Vault+Jenkins+Integration),
you can see a wiki on how to pull a secret from Vault into a Jenkinsfile.
Contact Hogan/Mark/SRE for adding the actual secret to Vault.

### Jenkinsfile Helm Example

Below is an example of the helm jenkins variable with a secret included (secrets.WPENGINE_APIKEY). This is utilizing the
[django-api](https://github.com/wpengine/helm-charts/tree/master/stable/django-api) shared helm chart.

``` shell
stage('Deploy Staging') {
                            def registryEnv = dockerRegistry.createDockerRegistry('corporate')
                            wrap([$class: 'VaultBuildWrapper', vaultSecrets: vault_secrets_development]) {
                                helm.deploy {
                                    wpeEnv = 'corporate-staging'
                                    releaseName = 'edge-api-staging'
                                    chart = 'wpengine/django-api'
                                    version = '2.2.1'
                                    values = [
                                        "app.image": registryEnv.getRemoteImage(IMAGE_NAME),
                                        "environment": "staging",
                                        "appName": "edge-api",
                                        "django_settings_module": "config.settings.staging",
                                        "secrets.WPENGINE_APIKEY": "$wpengine_apikey" # SECRET HERE!!!!!!
                                    ]
                                }
                            }
                        }
```

### Managed Kubernetes Secrets (helm chart relies on)

1. tls-wpesvc.net

The **tls-wpesvc.net** secret is a secret that can be shared by multiple projects.
It contains a wildcard certificate for \*.wpesvc.net in staging and production.

2. shared-cloudsql

The **shared-cloudsql** secret contains information for the app to connect
to the Cloud SQL database.

3. shared-newrelic

The **shared-newrelic** secret  contains a New Relic license key that needs to be available in order for the application
to report data.

[Helm]: https://github.com/kubernetes/helm
[Terraform]: https://www.terraform.io/
