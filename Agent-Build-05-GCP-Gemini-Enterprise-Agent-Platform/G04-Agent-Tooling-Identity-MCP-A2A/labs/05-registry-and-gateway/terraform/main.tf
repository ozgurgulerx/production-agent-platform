# G04 lab 05: bind the existing ticket-agent to an Agent Gateway (map I8: google-beta, agent_gateway_config,
# identity_type must be AGENT_IDENTITY). Status: scaffold only, functionality unverified.
terraform {
  required_providers {
    google-beta = { source = "hashicorp/google-beta", version = ">= 5.28.0" }
  }
}
variable "project" {}
variable "region" {}
variable "principal" {}

resource "google_vertex_ai_reasoning_engine" "ticket_agent" {
  provider     = google-beta
  project      = var.project
  region       = var.region
  display_name = "ticket-agent"
  # TODO(learner): import the existing resource (terraform import ... projects/P/locations/L/reasoningEngines/ID)
  # and fill spec from `gcloud ai reasoning-engines describe` so apply does not recreate it (a recreate mints a new principal, map D10).
  spec {
    agent_framework = "google-adk"
    # identity_type = "AGENT_IDENTITY"            # TODO(learner): confirm attribute name on the live Terraform page (map I8)
    # agent_gateway_config { ... }                # TODO(learner): gateway resource name once created (map F7, I8)
  }
}
