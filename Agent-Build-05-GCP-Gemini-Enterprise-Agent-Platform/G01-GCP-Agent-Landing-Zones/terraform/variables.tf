# Variables for the G01 scaffold. Values come from ../../.env (map labs-setup); copy them into
# a terraform.tfvars that is gitignored. Status 25 Oct 2026: scaffold only, functionality unverified.

variable "project_id" {
  type        = string
  description = "GOOGLE_CLOUD_PROJECT. Must already be inside the VPC-SC perimeter before any agent deploys (I2)."
}

variable "project_number" {
  type        = string
  description = "Numeric project number; needed to name the two service agents (I4, I6)."
}

variable "region" {
  type        = string
  default     = "europe-west2"
  description = "GOOGLE_CLOUD_LOCATION. Regional, never us/eu/global, when CMEK is mandated (A9, F5)."
}

variable "staging_bucket" {
  type        = string
  description = "Bucket name without gs://; same region as var.region (A9)."
}

variable "kms_key_name" {
  type        = string
  default     = ""
  description = "projects/P/locations/REGION/keyRings/R/cryptoKeys/K from the platform team; key ring in the same region (F5). Empty disables CMEK blocks."
}

variable "psc_subnetwork" {
  type        = string
  default     = ""
  description = "Self link of the /28 (or larger) subnet for the network attachment (I3). Empty skips the attachment."
}

variable "deployer_member" {
  type        = string
  description = "user:you@example.com or serviceAccount:cicd@P.iam.gserviceaccount.com; receives the I6 roles."
}

variable "ticket_mcp_url" {
  type        = string
  default     = ""
  description = "TICKET_MCP_URL, the Toolbox Cloud Run URL from G04 lab 03. Must be reachable over the PSC interface inside a perimeter (I2, I3)."
}

# TODO(learner): allowed_models list for constraints/vertexai.allowedModels (F6) when the org-policy
# resources are added; values look like publishers/google/models/gemini-3.5-flash:predict.
