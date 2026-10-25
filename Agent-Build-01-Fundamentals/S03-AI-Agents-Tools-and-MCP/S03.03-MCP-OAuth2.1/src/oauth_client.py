"""Discover local MCP/Keycloak endpoints and optionally run PKCE login."""

import argparse
import asyncio
import base64
import hashlib
import json
import queue
import secrets
import subprocess
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, unquote, urlencode, urlsplit
from urllib.request import (
    HTTPRedirectHandler,
    Request,
    build_opener,
    parse_http_list,
    parse_keqv_list,
)

MCP_URL = "http://127.0.0.1:8000/mcp"
EXPECTED_ISSUER = "http://127.0.0.1:9000/realms/s03-mcp"
CLIENT_ID = "s03-mcp-client"
REDIRECT_URI = "http://127.0.0.1:8765/callback"
REQUESTED_SCOPES = "openid tickets.read policies.read tickets.refund"


class NoRedirects(HTTPRedirectHandler):
    """Do not follow redirects from the explicitly trusted local services."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def require_local_url(value: str, base: str) -> str:
    """Restrict discovery URLs to a configured origin and path subtree."""
    if not isinstance(value, str):
        raise ValueError("Discovery is missing a required URL.")
    url, trusted = urlsplit(value), urlsplit(base)
    same_origin = (url.scheme, url.netloc) == (trusted.scheme, trusted.netloc)
    allowed_path = url.path == trusted.path or url.path.startswith(trusted.path + "/")
    unsafe_path = any(part in (".", "..") for part in unquote(url.path).split("/"))
    if not same_origin or not allowed_path or unsafe_path or url.query or url.fragment:
        raise ValueError("Discovery URL is outside the trusted local service.")
    return value


def request_json(url: str, form: dict | None = None) -> tuple[int, object, dict]:
    """Read bounded JSON with a timeout; retain an MCP 401 challenge."""
    headers = {"Accept": "application/json, text/event-stream"}
    data = None if form is None else urlencode(form).encode('ascii')
    if form is not None:
        headers = {**headers, "Content-Type": "application/x-www-form-urlencoded"}
    request = Request(url, data=data, headers=headers)
    try:
        response = build_opener(NoRedirects()).open(request, timeout=10)
    except HTTPError as error:
        response = error
    with response:
        if response.status not in (200, 401):
            raise ValueError(f"Request returned HTTP {response.status}.")
        raw = response.read(1_048_577)
        if len(raw) > 1_048_576:
            raise ValueError("Discovery response is too large.")
        body = json.loads(raw)
        if not isinstance(body, dict):
            raise ValueError("Discovery response must be a JSON object.")
        return response.status, response.headers, body


def read_metadata(url: str) -> dict:
    status, _, body = request_json(url)
    if status != 200:
        raise ValueError("Metadata must be publicly readable with HTTP 200.")
    return body


def discover() -> dict:
    """Follow our MCP challenge and Keycloak's OIDC discovery document."""
    status, headers, _ = request_json(MCP_URL)
    if status != 401:
        raise ValueError("Expected the protected MCP endpoint to return HTTP 401.")
    scheme, _, parameters = headers.get("WWW-Authenticate", "").partition(" ")
    if scheme.lower() != "bearer":
        raise ValueError("Expected a Bearer authentication challenge.")
    challenge = parse_keqv_list(parse_http_list(parameters))
    metadata_url = require_local_url(
        challenge.get("resource_metadata"), "http://127.0.0.1:8000"
    )
    resource = read_metadata(metadata_url)
    if resource.get("resource") != MCP_URL:
        raise ValueError("Protected-resource metadata identifies a different MCP server.")
    issuers = resource.get("authorization_servers")
    if not isinstance(issuers, list) or EXPECTED_ISSUER not in issuers:
        raise ValueError("MCP metadata does not advertise our trusted Keycloak realm.")

    # This local teaching client uses Keycloak's known OIDC discovery convention.
    metadata = read_metadata(EXPECTED_ISSUER + "/.well-known/openid-configuration")
    if metadata.get("issuer") != EXPECTED_ISSUER:
        raise ValueError("Discovered issuer does not match the trusted Keycloak realm.")
    methods = metadata.get("code_challenge_methods_supported")
    if not isinstance(methods, list) or "S256" not in methods:
        raise ValueError("Keycloak must advertise PKCE S256 support.")
    endpoints = {
        name: require_local_url(metadata.get(name), EXPECTED_ISSUER)
        for name in ("authorization_endpoint", "token_endpoint", "jwks_uri")
    }
    return {"resource": MCP_URL, "issuer": EXPECTED_ISSUER, **endpoints}


class LoginDenied(ValueError):
    """The authorization server returned a validated denial response."""


def pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode('ascii')).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b'=').decode('ascii')


def authorization_url(metadata: dict, verifier: str, state: str, user: str) -> str:
    endpoint = require_local_url(metadata['authorization_endpoint'], EXPECTED_ISSUER)
    parameters = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': REQUESTED_SCOPES,
        'resource': MCP_URL,
        'state': state,
        'code_challenge': pkce_challenge(verifier),
        'code_challenge_method': 'S256',
        'prompt': 'login',
        'login_hint': user,
    }
    return endpoint + '?' + urlencode(parameters)


def validate_callback(target: str, state: str) -> str:
    """Reject unsolicited, ambiguous or wrong-issuer authorization responses."""
    url = urlsplit(target)
    if url.path != '/callback' or url.scheme or url.netloc or url.fragment:
        raise ValueError('Unexpected callback path.')
    parameters = parse_qs(url.query, keep_blank_values=True, max_num_fields=20)
    if any(len(values) != 1 for values in parameters.values()):
        raise ValueError('Duplicate callback parameters.')
    supplied_state = parameters.get('state', [''])[0]
    if not secrets.compare_digest(supplied_state.encode(), state.encode()):
        raise ValueError('Callback state did not match.')
    if parameters.get('iss') != [EXPECTED_ISSUER]:
        raise ValueError('Callback issuer did not match.')
    if 'error' in parameters:
        if 'code' in parameters:
            raise ValueError('Ambiguous callback response.')
        raise LoginDenied('Keycloak did not authorize this login. Try again.')
    code = parameters.get('code', [''])[0]
    if not code:
        raise ValueError('Callback is missing the authorization code.')
    return code


def callback_handler(state: str, results: queue.SimpleQueue):
    """Use fixed browser messages and suppress query-string access logging."""
    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            self.request.settimeout(2)
            super().setup()

        def log_message(self, format, *args):
            pass  # Callback URLs contain authorization codes: never log them.

        def do_GET(self):
            try:
                if self.headers.get('Host') != '127.0.0.1:8765':
                    raise ValueError('Unexpected callback host.')
                result = validate_callback(self.path, state)
            except LoginDenied as error:
                results.put(error)
                self.respond(400, 'Login was not authorized. Return to the terminal.')
            except ValueError:
                self.respond(400, 'Invalid callback. The login is still waiting.')
            else:
                results.put(result)
                self.respond(200, 'Callback received. Return to the terminal for the token exchange result.')

        def respond(self, status, message):
            body = message.encode('utf-8')
            self.send_response(status)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Referrer-Policy', 'no-referrer')
            self.end_headers()
            self.wfile.write(body)

    return Handler


def receive_code(url: str, state: str, timeout: float = 300) -> str:
    """Bind before opening Safari; wait at most five minutes for login."""
    results = queue.SimpleQueue()
    with HTTPServer(('127.0.0.1', 8765), callback_handler(state, results)) as server:
        server.timeout = 1
        subprocess.run(['open', '-a', 'Safari', url], check=True, capture_output=True)
        print('Sign in in Safari. Waiting up to five minutes for the callback...', flush=True)
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            server.handle_request()
            try:
                result = results.get_nowait()
            except queue.Empty:
                continue
            if isinstance(result, LoginDenied):
                raise result
            return result
    raise TimeoutError('Login timed out. Run the login command again.')


def exchange_code(metadata: dict, code: str, verifier: str) -> dict:
    endpoint = require_local_url(metadata['token_endpoint'], EXPECTED_ISSUER)
    status, _, tokens = request_json(endpoint, form={
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'code': code,
        'code_verifier': verifier,
        'resource': MCP_URL,
    })
    if status != 200:
        raise ValueError('Keycloak rejected the token exchange.')
    if not isinstance(tokens.get('access_token'), str) or not tokens['access_token']:
        raise ValueError('Keycloak did not return an access token.')
    if str(tokens.get('token_type', '')).lower() != 'bearer':
        raise ValueError('Expected a Bearer access token.')
    return tokens


def token_summary(tokens: dict) -> dict:
    """Report receipt without printing access, refresh or ID tokens."""
    return {
        'token_received': True,
        'token_type': tokens.get('token_type'),
        'scope': tokens.get('scope'),
        'expires_in': tokens.get('expires_in'),
    }


def login(metadata: dict, user: str) -> dict:
    verifier = secrets.token_urlsafe(64)
    state = secrets.token_urlsafe(32)
    url = authorization_url(metadata, verifier, state, user)
    code = receive_code(url, state)
    return exchange_code(metadata, code, verifier)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--login', action='store_true', help='Open Safari for PKCE login')
    parser.add_argument('--user', choices=('ayse', 'mert'), default='ayse', help='Login hint only')
    parser.add_argument('--tool', choices=('get_ticket', 'list_tickets', 'get_policy', 'issue_refund'))
    parser.add_argument('--ticket-id', default='T-1003')
    parser.add_argument('--policy-id', default='POL-REFUND-01')
    parser.add_argument('--amount', default='100.00', help='GBP decimal string for simulated refund')
    args = parser.parse_args()
    try:
        metadata = discover()
        if args.login or args.tool:
            tokens = login(metadata, args.user)
            result = token_summary(tokens)
            if args.tool:
                from mcp_demo import call_tool
                arguments = {
                    'get_ticket': {'ticket_id': args.ticket_id},
                    'list_tickets': {},
                    'get_policy': {'policy_id': args.policy_id},
                    'issue_refund': {'ticket_id': args.ticket_id, 'amount': args.amount},
                }[args.tool]
                tool_result = asyncio.run(call_tool(tokens['access_token'], args.tool, arguments))
                result = {**result, 'tool_result': tool_result}
        else:
            result = metadata
        print(json.dumps(result, indent=2))
    except subprocess.CalledProcessError:
        raise SystemExit('Could not open Safari. Check that it is installed and retry.') from None
    except (ValueError, URLError, OSError) as error:
        raise SystemExit(f'OAuth step failed: {error}') from None
    except ExceptionGroup:
        raise SystemExit('MCP request failed. Check that the updated server is running and accepts the token.') from None
    except KeyboardInterrupt:
        raise SystemExit('Login cancelled.') from None


if __name__ == '__main__':
    main()
