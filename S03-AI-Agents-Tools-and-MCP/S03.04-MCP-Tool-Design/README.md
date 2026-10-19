# MCP Tool Design 

“How would you expose our systems to an agent?” is one of the most common architect questions. The weak answer is “wrap the APIs as tools”. The strong answer is “I’d start from what the agent needs to get done, build a small set of intent-level tools with precise descriptions, keep the deterministic logic in code, and measure wrong-tool rate before adding more.” Each clause of that answer maps to one of the four decisions above.

Exposing each API endpoint as an MCP tool is an anti-pattern. 
We need to move individual endpoints to intent-shaped tool sets.


Having more agents means the LLM would need to understand which to use when, and in what order. In that sense having a large set of tool makes LLMs job difficult. 

- Ambiguous selection: Several tools appear suitable, with subtle differences buried in descriptions.
- Longer, fragile workflows: The agent must assemble many small operations; each step creates another opportunity for a mistake. We should avoid making the agent reconstruct predictable, complicated workflows dynamically in production and move such workflows to code.
- Attention overhead: More definitions compete with the user’s request and the evidence needed to solve it.

Consider the following example...

An API-shaped tool set might expose list_calendars, list_events, get_event, get_attendees, check_availability, patch_event, send_email, and dozens more. The agent must figure out which operations belong together, their order, and details such as whether changing the event already notifies attendees.

An intent-shaped tool set might expose find_meeting, find_available_times, and reschedule_meeting. These still need precise inputs and safeguards, but they put more of the workflow’s reliable mechanics into software.