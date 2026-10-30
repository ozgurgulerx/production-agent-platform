# Values come from the track-root .env; pass with -var on the command line (lab README step 6).

variable "project_id" {
  type        = string
  description = "GOOGLE_CLOUD_PROJECT"
}

variable "region" {
  type        = string
  default     = "europe-west2"
  description = "GOOGLE_CLOUD_LOCATION; regional (map A9)"
}

variable "staging_bucket" {
  type        = string
  description = "AGENT_RUNTIME_STAGING_BUCKET without gs://; same region (A9)"
}

variable "ticket_mcp_url" {
  type        = string
  default     = ""
  description = "TICKET_MCP_URL from G04 lab 03; empty uses the stub tools in agent.py"
}
