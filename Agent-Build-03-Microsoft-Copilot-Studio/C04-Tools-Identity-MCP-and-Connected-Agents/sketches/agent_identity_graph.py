"""Shape only: the Graph queries that reveal a Copilot Studio agent's Entra Agent ID (reading map E1).

Not run. Every agent identity is a service principal created under the Microsoft-owned blueprint
"Microsoft Copilot Studio agent identity blueprint" (app id 25664c89-cea5-4ab6-b924-a54fd8a19ae0).
The filter spellings below follow the Graph beta agent-identity surface and are marked verify.
"""

BLUEPRINT_APP_ID = "25664c89-cea5-4ab6-b924-a54fd8a19ae0"

# 1. The blueprint itself (one per tenant, appears after the first agent is created).
BLUEPRINT = f"/v1.0/servicePrincipals?$filter=appId eq '{BLUEPRINT_APP_ID}'"

# 2. Agent identities by display name (the agent's name in Copilot Studio). Simplest, works on v1.0.
BY_NAME = "/v1.0/servicePrincipals?$filter=displayName eq '{agent_name}'&$select=id,appId,displayName,createdDateTime,servicePrincipalType,tags"

# 3. Agent identities by subtype (beta; the property name may differ, verify):
BY_SUBTYPE = "/beta/servicePrincipals?$filter=servicePrincipalType eq 'Agent'&$count=true"   # verify: header ConsistencyLevel: eventual

# 4. What the identity may do: delegated grants and app-role assignments (connector scopes attached on publish).
GRANTS = "/v1.0/servicePrincipals/{sp_id}/oauth2PermissionGrants"
APP_ROLES = "/v1.0/servicePrincipals/{sp_id}/appRoleAssignments"

# 5. Sponsor (owner) of the agent identity (beta; verify the relationship name).
SPONSORS = "/beta/servicePrincipals/{sp_id}/sponsors"   # verify

if __name__ == "__main__":
    for name, q in [("blueprint", BLUEPRINT), ("by name", BY_NAME), ("by subtype", BY_SUBTYPE),
                    ("grants", GRANTS), ("app roles", APP_ROLES), ("sponsors", SPONSORS)]:
        print(f"{name:11} {q}")
