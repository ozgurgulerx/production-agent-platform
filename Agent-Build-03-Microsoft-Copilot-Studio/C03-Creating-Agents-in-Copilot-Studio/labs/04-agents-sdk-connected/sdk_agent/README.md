# sdk_agent — run, tunnel, register

```bash
source ../../../../labs-setup/.venv/bin/activate
export CONNECTIONS__SERVICE_CONNECTION__SETTINGS__CLIENTID=<bot app id>     # from the Azure Bot registration
export CONNECTIONS__SERVICE_CONNECTION__SETTINGS__TENANTID=$TENANT_ID
export CONNECTIONS__SERVICE_CONNECTION__SETTINGS__AUTHTYPE=federated_credentials   # or user_managed_identity when hosted on Azure; never client_secret here
export CONNECTIONS__SERVICE_CONNECTION__SETTINGS__FEDERATEDCLIENTID=<managed identity client id>
python app.py
```
Local smoke test without auth (anonymous mode, see `app.py`):
```bash
curl -s -X POST localhost:3978/api/messages -H 'content-type: application/json' \
  -d '{"type":"message","text":"what is the SLA for P1 tickets?","from":{"id":"u1"},"recipient":{"id":"bot"},"conversation":{"id":"c1"},"channelId":"test","serviceUrl":"http://localhost:3978"}'
```
Tunnel: `devtunnel host -p 3978 --allow-anonymous` (or ngrok). Azure Bot: create a Bot resource (user-assigned managed identity or single-tenant app with a federated credential), messaging endpoint `https://<tunnel>/api/messages`, Teams channel optional. The Agents Playground (`npx @microsoft/agents-playground`, verify name) can drive the local endpoint.
