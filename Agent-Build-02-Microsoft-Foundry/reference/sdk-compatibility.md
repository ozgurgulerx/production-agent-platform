# SDK compatibility and verification status

Reviewed from repository declarations on 30 October 2026; no installation, upgrade or runtime validation was performed.

| Environment | Declared constraint or package | Status |
|---|---|---|
| Shared labs-setup | azure-ai-projects 2.7.0; agent-framework-foundry 1.15.0; agent-framework-core 1.23.0 | Existing declarations retained, not newly tested |
| Evaluation lab | Existing documentation specifies Projects 2.9.0 and a separate environment | Preserve separation; resolve from that lab’s instructions |
| Hosting | Existing shared requirements contain beta hosting/server packages | Check compatibility before a build; no GA inference from a version string |

The existing reading map records a framework dependency ceiling below Projects 2.8. Treat this as dated repository evidence, not a current package-manager resolution. Do not upgrade all environments together. Record Python, exact dependencies, API generation, endpoint, CLI/extension versions, check date, and result separately for each exercised environment.

The structural move preserved local environments. Virtual-environment activation files and executable shebangs may embed their former absolute paths: recreate an environment from its existing declarations when needed rather than assume moving it keeps it runnable. No environment is deleted or silently repaired by this documentation update.

New stages must be self-contained. Existing shared environments are preserved as legacy structure pending an explicit environment migration. No stage should import another stage’s implementation.

Official references: [Foundry SDK overview](https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/sdk-overview), [Agent migration](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/migrate). The original reading map is retained as historical provenance; its preview, retirement and availability claims require dated confirmation before use.
