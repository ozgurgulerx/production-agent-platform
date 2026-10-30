"""Shape of the quarantine calls on the Power Platform API (F5). Not run.

POST {POWER_PLATFORM_API}/copilotstudio/environments/{environmentId}/bots/{botId}/botQuarantine/SetAsQuarantined?api-version=2022-03-01-preview
POST {POWER_PLATFORM_API}/copilotstudio/environments/{environmentId}/bots/{botId}/botQuarantine/SetAsUnquarantined?api-version=2022-03-01-preview   # verify: release operation name and api-version from F5
Requires: Global / AI / Power Platform admin and the delegated scope CopilotStudio.AdminActions.Invoke on the Power Platform API.
Effect: every channel stops; the agent answers only in the maker's test pane; inventory shows isQuarantined=true (E7).
"""
QUARANTINE = {
    "method": "POST",
    "url": "{api}/copilotstudio/environments/{env}/bots/{bot}/botQuarantine/SetAsQuarantined",
    "params": {"api-version": "2022-03-01-preview"},   # verify
    "headers": {"Authorization": "Bearer <token with CopilotStudio.AdminActions.Invoke>"},
    "body": None,
}
RELEASE = dict(QUARANTINE, url="{api}/copilotstudio/environments/{env}/bots/{bot}/botQuarantine/SetAsUnquarantined")   # verify
INVENTORY_FIELDS_TO_CHECK_AFTER = ["isQuarantined", "authenticationMode", "entireTenant", "connectionProvider"]
