# S03.03: MCP + OAuthv2.1 Authorization for Tools / Resouces Access

## What we are going to build
In S03.01 we built the python functions.
In S03.02 we exposed them as MCP tools through an MCP server we created with FastMCP. 
An LLM Agent was able to discover the capabilities and call / use these tool through the MCP server.

Now in S03.03 we will make the tools to be callable by the right person. 
We will keep the existing tool and add a issue_refund tool, using Ayşe (support agent) and Mert (supervisor) to demonstrate scope enforcement, server side policy checks and human confirmation.

## Authorization acceptance tests

These are planned checks, not completed evidence.

- [ ] No token → HTTP 401 with a protected-resource metadata challenge.
- [ ] Expired access token → HTTP 401; tool does not execute.
- [ ] Invalid signature → HTTP 401; tool does not execute.
- [ ] Wrong audience (`aud`) → HTTP 401; tool does not execute.
- [ ] ID token used as an access token → HTTP 401, even if signed by the trusted authorization server.
- [ ] Ayşe calls issue_refund → HTTP 403 insufficient_scope; no refund recorded.
- [ ] Downstream request → incoming bearer token is never forwarded.

### Vocabulary used in this stage


## Tests
```python
python3 -m pytest tests/test_refund_policy.py -q
```

## Current progress
