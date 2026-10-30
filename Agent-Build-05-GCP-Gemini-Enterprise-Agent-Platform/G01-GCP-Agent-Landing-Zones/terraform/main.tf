# G01 landing-zone scaffold for the ticket agent on Agent Runtime.
# Read, do not apply. Status 25 Oct 2026: scaffold only, functionality unverified.
# Every fact cites the reading map (../../reference/reading-map-gcp-agents-2026-10-25.md).
# The perimeter, the Shared VPC and the KMS key ring belong to the platform tier (I1);
# they are referenced here by variable, not created.

terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.28.0" # google_vertex_ai_reasoning_engine (I8)
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = ">= 5.28.0" # agent_gateway_config only (I8); unused in this scaffold
    }
  }
  # TODO(learner): backend "gcs" {} in the platform-owned state bucket.
}

provider "google" {
  project = var.project_id
  region  = var.region
}

locals {
  # The two service agents (I4, I6). Both are Google-created on first use.
  runtime_service_agent  = "service-${var.project_number}@gcp-sa-aiplatform-re.iam.gserviceaccount.com"
  platform_service_agent = "service-${var.project_number}@gcp-sa-aiplatform.iam.gserviceaccount.com"
}

# --- APIs (I6) -----------------------------------------------------------------
resource "google_project_service" "apis" {
  for_each = toset([
    "aiplatform.googleapis.com",
    "storage.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com",
    "telemetry.googleapis.com",
    "cloudtrace.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "cloudkms.googleapis.com",
    "artifactregistry.googleapis.com",
  ])
  service            = each.value
  disable_on_destroy = false
}

# --- IAM for the two service agents ---------------------------------------------
# Runtime service agent pulls custom images; the reasoning engine must depend_on this
# binding or the first deploy ends in IMAGE_PULL_BACKOFF (I8).
resource "google_project_iam_member" "runtime_agent_ar_reader" {
  project = var.project_id
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:${local.runtime_service_agent}"
  # TODO(learner): confirm the service agent exists (first deploy creates it) before applying.
}

# Platform service agent holds the CMEK role (I4).
resource "google_kms_crypto_key_iam_member" "platform_agent_cmek" {
  count         = var.kms_key_name == "" ? 0 : 1
  crypto_key_id = var.kms_key_name
  role          = "roles/cloudkms.cryptoKeyEncrypterDecrypter"
  member        = "serviceAccount:${local.platform_service_agent}"
}

# Your deployer identity (I6). Narrow in production; this is the set-up page's list.
resource "google_project_iam_member" "deployer" {
  for_each = toset([
    "roles/aiplatform.user",
    "roles/aiplatform.agentContextEditor",
    "roles/aiplatform.agentDefaultAccess",
    "roles/iam.serviceAccountUser",
    "roles/storage.admin",
  ])
  project = var.project_id
  role    = each.value
  member  = var.deployer_member
}

# --- Network attachment for the PSC interface (I3) -----------------------------
# /28 minimum; cannot be changed on the agent without recreating it.
resource "google_compute_network_attachment" "agent_runtime" {
  count                 = var.psc_subnetwork == "" ? 0 : 1
  name                  = "ticket-agent-psc"
  region                = var.region
  connection_preference = "ACCEPT_AUTOMATIC"
  subnetworks           = [var.psc_subnetwork]
  # TODO(learner): producer_accept_lists for the Runtime producer project if the platform team
  # requires ACCEPT_MANUAL (unverified in the map; ask them).
}

# --- Staging bucket in the same region (A9, F5) --------------------------------
resource "google_storage_bucket" "staging" {
  name                        = var.staging_bucket
  location                    = upper(var.region)
  uniform_bucket_level_access = true
  dynamic "encryption" {
    for_each = var.kms_key_name == "" ? [] : [1]
    content {
      default_kms_key_name = var.kms_key_name
    }
  }
}

# --- Audit logs: Data Access is off until enabled (F8) -------------------------
resource "google_project_iam_audit_config" "aiplatform" {
  project = var.project_id
  service = "aiplatform.googleapis.com"
  audit_log_config { log_type = "DATA_READ" }
  audit_log_config { log_type = "DATA_WRITE" }
}

# --- The agent itself (I8) -------------------------------------------------------
# Objects under pickle_object_gcs_uri and requirements_gcs_uri are produced by the SDK path
# (G03 lab 02) or the G02 pipeline; they do not exist yet.
resource "google_vertex_ai_reasoning_engine" "ticket_agent" {
  display_name = "ticket-agent"
  region       = var.region
  description  = "Support-ticket agent; refuses refunds outside policy."

  spec {
    agent_framework = "google-adk"
    package_spec {
      python_version       = "3.13"
      pickle_object_gcs_uri = "gs://${var.staging_bucket}/ticket-agent/agent.pkl"     # TODO(learner)
      requirements_gcs_uri  = "gs://${var.staging_bucket}/ticket-agent/requirements.txt" # TODO(learner)
    }
    deployment_spec {
      env {
        name  = "TICKET_MCP_URL"
        value = var.ticket_mcp_url
      }
      env {
        name  = "GOOGLE_GENAI_USE_VERTEXAI"
        value = "TRUE"
      }
      # TODO(learner): secret_env for anything that is a secret; never a plain env.
    }
    # TODO(learner): service_account is omitted on purpose; the labs use Agent Identity
    # (identity_type=AGENT_IDENTITY, C5). Check the provider's field name for identity_type
    # against I8 before adding it (unverified in the map).
  }

  # TODO(learner): encryption_spec { kms_key_name = var.kms_key_name } once the provider
  # field is confirmed (F5 names encryptionSpec.kmsKeyName on the API).

  depends_on = [
    google_project_service.apis,
    google_project_iam_member.runtime_agent_ar_reader, # I8
  ]
}

output "agent_runtime_resource" {
  description = "Paste into .env as AGENT_RUNTIME_RESOURCE"
  value       = google_vertex_ai_reasoning_engine.ticket_agent.id
}
