variable "gcp_project" {
  description = "The GCP project to create resources in"
  default     = "wp-engine-corporate"
}

variable "gcp_region" {
  description = "The GCP region to create resources in"
  default     = "us-east1"
}

variable "k8s_context" {
  description = "The k8s config context to use"
  default     = "gke_wp-engine-corporate_us-east1-c_us-east1-prod-01"
}

variable "db_password" {
  description = "The password for the database app user"
}
