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
      description = "namespace for generated project (staging), digitalocean-builder"
    }
    name = "digitalocean-builder"
  }
}

module "db-for-k8s" {
  source = "git@github.com:wpengine/infraform.git//modules/db-for-k8s"

  name        = "digitalocean-builder-staging-1"
  db_name     = "digitalocean-builder"
  app_name    = "digitalocean-builder"
  namespace   = "${kubernetes_namespace.project_namespace.id}"
  db_password = "${var.db_password}"
}
