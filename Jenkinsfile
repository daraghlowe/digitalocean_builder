#!groovy
@Library('wpshared') _

node('docker') {
    // This pipeline var does nice things like automatically cleanup your workspace and hipchat the provided room
    // when master builds fail. Docs are available at:
    // https://jenkins.wpengine.io/job/WPEngineGitHubRepos/job/jenkins_shared_library/job/master/pipeline-syntax/globals#wpe
    wpe.pipeline('hut') {
        String  IMAGE_NAME = "digitalocean-builder:${DOCKER_TAG}"

        // IMAGE_TAG is used in docker-compose to ensure uniqueness of containers and networks.
        // COMPOSE_PROJECT_NAME is used to name the docker-compose network and images. It defaults to the current
        // directory which is dangerous in Jenkins because somethings this can start with invalid characters
        withEnv(["IMAGE_TAG=:${DOCKER_TAG}",
                 "COMPOSE_PROJECT_NAME=digitalocean-builder-${DOCKER_TAG}"]) {
            try {
                stage('Build') {
                	// Build all of the images
                    sh 'make build'
                }

                stage('Test') {
                    sh 'make clean-artifacts test generate-openapi'
                    junit 'digitalocean-builder/artifacts/junit.xml'
                    coverage.publish 'digitalocean-builder/artifacts/coverage.xml'
                    publishHTML (target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: 'digitalocean-builder/artifacts/coverage',
                        reportFiles: 'index.html',
                        reportName: 'Test Coverage'
                    ])
                }

                if (env.BRANCH_NAME == 'master') {
                    milestone 1
                    // Only allow one deploy at a time
                    lock(resource: 'digitalocean-builder_deploy', inversePrecedence:true) {
                        // Any older builds that reach milestone after a more recent build will be aborted
                        milestone 2

                        stage('Publish To Corporate Registry') {
                            // Tag the images from make build with the registry appropriate names
                            dockerRegistry.publishImage {
                                environment = 'corporate'
                                image = IMAGE_NAME
                            }
                        }

                        stage('Terraform Staging') {
                            withCredentials([string(credentialsId: 'digitalocean-builder-staging-db-password', variable: 'TF_VAR_db_password')]) {
                                terraform.apply {
                                    terraformDir = "./deploy/terraform/staging"
                                    hipchatRoom = "hut"
                                    envVars = ['TF_VAR_db_password']
                                }
                            }
                        }

                        // stage('Deploy Cloud Endpoints Staging') {
                        //     endpoints.deploy {
                        //         wpeEnv = "corporate-staging"
                        //         openapiYaml = "./digitalocean-builder/artifacts/swagger-staging.yml"
                        //     }
                        // }

                        stage('Deploy Staging') {
                            // String endpointsConfigId = endpoints.latestConfigId {
                            //     wpeEnv = 'corporate-staging'
                            //     service = 'digitalocean-builder-staging.endpoints.wp-engine-corporate.cloud.goog'
                            // }
                            def registryEnv = dockerRegistry.createDockerRegistry('corporate')

                            withCredentials([
                                string(credentialsId: 'digitalocean-builder-redis-password', variable: 'REDIS_PASSWORD'),
                                // string(credentialsId: 'digitalocean-builder-rollbar-token', variable: 'ROLLBAR_ACCESS_TOKEN')
                                string(credentialsId: 'K8S_CORPORATE_SHARED_NEW_RELIC_LICENSE_KEY_STAGING', variable: 'NEW_RELIC_LICENSE_KEY'),
                                string(credentialsId: 'K8S_CORPORATE_SHARED_CLOUD_SQL_SVC_ACCT_KEY_B64_STAGING', variable: 'CLOUD_SQL_SVC_ACCOUNT_KEY_B64'),
                                string(credentialsId: 'TLS_WPESVC_NET_CRT_B64', variable: 'TLS_WPESVC_NET_CRT_B64'),
                                string(credentialsId: 'TLS_WPESVC_NET_KEY_B64', variable: 'TLS_WPESVC_NET_KEY_B64')
                            ]) {
                                // See https://github.com/wpengine/helm-charts/tree/master/stable/django-api for possible values to set
                                helm.deploy {
                                    wpeEnv = 'corporate-staging'
                                    namespace = 'digitalocean-builder'
                                    releaseName = 'digitalocean-builder-staging'
                                    chart = 'wpengine/django-api'
                                    version = '2.10.3'
                                    values = [
                                        "app.image": registryEnv.getRemoteImage(IMAGE_NAME),
                                        "celeryWorker.image": registryEnv.getRemoteImage(IMAGE_NAME),
                                        "celeryScheduler.image": registryEnv.getRemoteImage(IMAGE_NAME),
                                        "redis.password": REDIS_PASSWORD,
                                        // "secrets.ROLLBAR_ACCESS_TOKEN": ROLLBAR_ACCESS_TOKEN
                                        // "gcp_endpoints.configId": endpointsConfigId,
                                        "cloud_sql_service_account_key_b64": CLOUD_SQL_SVC_ACCOUNT_KEY_B64,
                                        "newrelic_license_key": NEW_RELIC_LICENSE_KEY,
                                        "tls_wpesvc_net_cert_b64.crt": TLS_WPESVC_NET_CRT_B64,
                                        "tls_wpesvc_net_cert_b64.key": TLS_WPESVC_NET_KEY_B64
                                    ]
                                    valuesFiles = ["deploy/helm-values/staging.yaml"]
                                }
                            }
                        }

                        stage('Deploy Dashboards to Dev'){
                            grafana.deployDashboards {
                                dashboard_location = "${env.WORKSPACE}/deploy/grafana"
                                environment = 'farm-integration'
                            }
                        }

                        stage('Smoke Test Staging') {
                            sh "make smoke-test-staging"
                            junit 'digitalocean-builder/artifacts/smoke-tests-digitalocean-builder-staging.xml'
                        } // end smokes test staging

                        stage('Terraform Production') {
                            withCredentials([string(credentialsId: 'digitalocean-builder-production-db-password', variable: 'TF_VAR_db_password')]) {
                                terraform.apply {
                                    terraformDir = "./deploy/terraform/production"
                                    hipchatRoom = "hut"
                                    envVars = ['TF_VAR_db_password']
                                }
                            }
                        }

                        // stage('Deploy Cloud Endpoints Production') {
                        //     endpoints.deploy {
                        //         wpeEnv = 'corporate-production'
                        //         openapiYaml = './digitalocean-builder/artifacts/swagger-production.yml'
                        //     }
                        // }

                        stage('Deploy Production') {
                            // String endpointsConfigId = endpoints.latestConfigId {
                            //     wpeEnv = 'corporate-production'
                            //     service = 'digitalocean-builder-production.endpoints.wp-engine-corporate.cloud.goog'
                            // }
                            def registryEnv = dockerRegistry.createDockerRegistry('corporate')

                            withCredentials([
                                string(credentialsId: 'digitalocean-builder-redis-password', variable: 'REDIS_PASSWORD'),
                                // string(credentialsId: 'digitalocean-builder-rollbar-token', variable: 'ROLLBAR_ACCESS_TOKEN')
                                string(credentialsId: 'K8S_CORPORATE_SHARED_NEW_RELIC_LICENSE_KEY', variable: 'NEW_RELIC_LICENSE_KEY'),
                                string(credentialsId: 'K8S_CORPORATE_SHARED_CLOUD_SQL_SVC_ACCT_KEY_B64', variable: 'CLOUD_SQL_SVC_ACCOUNT_KEY_B64'),
                                string(credentialsId: 'TLS_WPESVC_NET_CRT_B64', variable: 'TLS_WPESVC_NET_CRT_B64'),
                                string(credentialsId: 'TLS_WPESVC_NET_KEY_B64', variable: 'TLS_WPESVC_NET_KEY_B64')
                            ]) {
                                // See https://github.com/wpengine/helm-charts/tree/master/stable/django-api for possible values to set
                                helm.deploy {
                                    wpeEnv = 'corporate-production'
                                    namespace = 'digitalocean-builder'
                                    releaseName = 'digitalocean-builder-production'
                                    chart = 'wpengine/django-api'
                                    version = '2.10.3'
                                    values = [
                                        "app.image": registryEnv.getRemoteImage(IMAGE_NAME),
                                        "celeryWorker.image": registryEnv.getRemoteImage(IMAGE_NAME),
                                        "celeryScheduler.image": registryEnv.getRemoteImage(IMAGE_NAME),
                                        "redis.password": REDIS_PASSWORD,
                                        // "secrets.ROLLBAR_ACCESS_TOKEN": ROLLBAR_ACCESS_TOKEN
                                        // "gcp_endpoints.configId": endpointsConfigId,
                                        "cloud_sql_service_account_key_b64": CLOUD_SQL_SVC_ACCOUNT_KEY_B64,
                                        "newrelic_license_key": NEW_RELIC_LICENSE_KEY,
                                        "tls_wpesvc_net_cert_b64.crt": TLS_WPESVC_NET_CRT_B64,
                                        "tls_wpesvc_net_cert_b64.key": TLS_WPESVC_NET_KEY_B64
                                    ]
                                    valuesFiles = ["deploy/helm-values/production.yaml"]
                                }
                            }
                        }

                        stage('Deploy Dashboards to Prod'){
                            grafana.deployDashboards {
                                dashboard_location = "${env.WORKSPACE}/deploy/grafana"
                                environment = 'corporate-production'
                            }
                        }

                        stage('Smoke Test Production') {
							sh "make smoke-test-production"
                            junit 'digitalocean-builder/artifacts/smoke-tests-digitalocean-builder.xml'
                        } // end smokes test production

                        // Update the :latest tag for the new image. This is used only for examples or someone trying out the image locally
                        dockerRegistry.publishImage {
                            environment = 'corporate'
                            image = IMAGE_NAME
                            updateLatest = true
                        }
                    } // end lock
                } // end if (env.BRANCH_NAME == 'master')
            }
            finally {
            	stage('Clean Up') {
                	sh 'docker-compose down'
                }
            }
        }
    }
}
