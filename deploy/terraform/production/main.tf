provider "google" {
  project = "${var.gcp_project}"
  region  = "${var.gcp_region}"
}

provider "kubernetes" {
  config_context = "${var.k8s_context}"
}

resource "kubernetes_namespace" "project_namespace" {
  metadata {
    annotations {
      description = "namespace for generated project, digitalocean-builder"
    }
    name = "digitalocean-builder"
  }
}

# adding a 2 to the end of db name bc cloud sql doesn't let you re-use names for a week
# will change this back to 1 after a week for example-django-microservice 7/13
module "db-for-k8s" {
  source = "git@github.com:wpengine/infraform.git//modules/db-for-k8s"

  name                     = "digitalocean-builder-prod-2"
  db_name                  = "digitalocean-builder"
  enable_backups           = "true"
  enable_high_availability = "true"
  app_name                 = "digitalocean-builder"
  namespace                = "${kubernetes_namespace.project_namespace.id}"
  db_password              = "${var.db_password}"
}
