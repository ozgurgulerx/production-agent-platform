# F11 capability builds — Copilot, Agent 365 and M365 boundaries

## Build contract

Status: **planned; functionality unverified**. Build one capability at a time using the existing module and labs. Record environment/dependency versions, permitted assistance, positive and negative results, and trace/test evidence. The learner writes code and tests; these contracts do not supply hidden implementations. Verify dated API and availability claims before execution.

### Publish and consume a Foundry agent

- [ ] Build: Demonstrate one supported Foundry-to-M365/Copilot publishing path with explicit tenant, agent version, authentication and ownership. Include private-network constraints as a separate verified compatibility question.
- [ ] Verify: Test denied consent, inaccessible project/data, removed access and rollback; do not assume portal publish success proves end-user authorization.

### Graph and low-code boundary

- [ ] Build: Implement a bounded Graph call with delegated permissions and compare app-only permissions. Map Copilot Studio topics, knowledge/actions, DLP and ALM to pro-code Foundry responsibilities; use companion Copilot folder for detailed authoring.
- [ ] Verify: Test least-privilege consent and throttling, and demonstrate permissions on SharePoint/Teams grounding. Record which environment and connection owns the access.

### Agent 365 governance handoff

- [ ] Build: Inspect supported registration/inventory/lifecycle integration and record operational owner, audit trail and access review. Separate service availability from source checklist claims.
- [ ] Verify: Produce a controlled integration walkthrough and an unavailable-feature path; no broad tenant changes or production rollout are implied.

## Exact checklist targets

Each ID below is a distinct occurrence in the [full coverage matrix](../reference/production-build-coverage.md). Source wording is retained, including historical names and unfinished placeholders; it is not a fresh API guarantee. Compound items may require several small builds. Mark complete only after recording evidence.

- [ ] **CB061** — azd ai agent publish, and publish through Microsoft 365
- [ ] **CB071** — Copilot Studio: low-code agents, grounding on SharePoint/Dataverse/AI Search, topics, generative orchestration, Power Platform connectors, governance via Power Platform admin centre and DLP, when to escalate to a pro-code Foundry agent, how the two interoperate (Copilot Studio calling Foundry agents / MCP, Foundry agents published to M365 Copilot). Two of the three £800 ads require it.
- [ ] **CB095** — Microsoft Agent 365 Integration with Foundry [link](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/agent-365-integration)
- [ ] **CB099** — publish & share [link](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/publish-copilot?tabs=portal)
- [ ] **CB100** — publish with a virtual network
- [ ] **CB218** — M365 Copilot extensibility (declarative agents, custom engine agents, Copilot connectors / Graph connectors), Copilot Studio agents published to Teams/M365, SharePoint grounding and oversharing risk (Purview, Restricted SharePoint Search), licensing basics, adoption governance. Hays £800 says Copilot must-have.
- [ ] **CB219** — App-only vs delegated permissions, consent, `GraphServiceClient`, reading mail/calendar/SharePoint/Teams on behalf of the user, throttling; needed for M365-facing agents (Access Computer Consulting, Copilot-adjacent ads).
- [ ] **CB220** — Copilot Studio and Power Platform surface — Copilot Studio agent authoring (topics, generative orchestration, knowledge sources, actions calling Foundry/MCP/REST), Power Platform CLI (`pac`) for ALM of agents, Dataverse basics, DLP policies; declarative agents for M365 Copilot via Teams Toolkit / Agents Toolkit (manifest JSON). Read and demo level, not daily coding.

## Completion evidence

- [ ] Store the artifact path, reproducible command, observed outcome, limitations and next gap in the existing study log.
- [ ] Preserve current labs; link to shared concepts rather than importing another stage’s implementation.
- [ ] Do not label a sample, empty test collection or planned experiment as verified functionality.
