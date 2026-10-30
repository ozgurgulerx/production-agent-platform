# Terraform variant of the deploy step (map I8). Plan only in the lab; nothing applied.
# The pickle and requirements objects must already exist in the staging bucket (uploaded by the SDK or
# CLI path). Revisions and traffic are managed from sketches/traffic_split.py; whether the provider
# exposes them is unverified. Status 25 Oct 2026: scaffold only, functionality unverified.

terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.28.0" # google_vertex_ai_reasoning_engine (I8)
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

data "google_project" "this" {}

# I8: the engine must depend on this binding or the first apply can IMAGE_PULL_BACKOFF.
resource "google_project_iam_member" "runtime_agent_ar_reader" {
  project = var.project_id
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:service-${data.google_project.this.number}@gcp-sa-aiplatform-re.iam.gserviceaccount.com"
}

resource "google_vertex_ai_reasoning_engine" "ticket_agent" {
  display_name = "ticket-agent"
  region       = var.region
  description  = "Support-ticket agent; refuses refunds outside policy."

  spec {
    agent_framework = "google-adk"
    package_spec {
      python_version        = "3.13"
      pickle_object_gcs_uri = "gs://${var.staging_bucket}/ticket-agent/agent.pkl"        # TODO(learner): produced by the SDK path
      requirements_gcs_uri  = "gs://${var.staging_bucket}/ticket-agent/requirements.txt" # TODO(learner)
    }
    deployment_spec {
      env {
        name  = "GOOGLE_GENAI_USE_VERTEXAI"
        value = "TRUE"
      }
      env {
        name  = "TICKET_MCP_URL"
        value = var.ticket_mcp_url
      }
    }
    # TODO(learner): identity_type AGENT_IDENTITY; field name in the provider unverified (I8 names it only
    # as a requirement for agent_gateway_config). No service_account on purpose (C5).
  }

  depends_on = [google_project_iam_member.runtime_agent_ar_reader]
}

output "agent_runtime_resource" {
  value = google_vertex_ai_reasoning_engine.ticket_agent.id
}
