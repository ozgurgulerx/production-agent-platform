import unittest
from unittest.mock import patch
import oauth_client as client

RESOURCE_METADATA = 'http://127.0.0.1:8000/.well-known/oauth-protected-resource/mcp'
ISSUER = 'http://127.0.0.1:9000/realms/s03-mcp'
AUTH = ISSUER + '/protocol/openid-connect/auth'
TOKEN = ISSUER + '/protocol/openid-connect/token'
JWKS = ISSUER + '/protocol/openid-connect/certs'
CHALLENGE = {'WWW-Authenticate': 'Bearer error="invalid_token", resource_metadata="' + RESOURCE_METADATA + '"'}
RESOURCE = {'resource': client.MCP_URL, 'authorization_servers': [ISSUER]}
METADATA = {'issuer': ISSUER, 'authorization_endpoint': AUTH, 'token_endpoint': TOKEN, 'jwks_uri': JWKS, 'code_challenge_methods_supported': ['S256']}

class DiscoveryTests(unittest.TestCase):
    def run_discovery(self, resource=RESOURCE, metadata=METADATA, challenge=CHALLENGE, status=401):
        with patch.object(client, 'request_json', side_effect=[(status, challenge, {}), (200, {}, resource), (200, {}, metadata)]):
            return client.discover()

    def test_discovers_expected_endpoints(self):
        result = self.run_discovery()
        self.assertEqual(result['token_endpoint'], TOKEN)
        self.assertEqual(result['authorization_endpoint'], AUTH)

    def test_rejects_wrong_resource(self):
        with self.assertRaises(ValueError):
            self.run_discovery(resource={**RESOURCE, 'resource': 'http://other/mcp'})

    def test_rejects_untrusted_issuer(self):
        with self.assertRaises(ValueError):
            self.run_discovery(resource={**RESOURCE, 'authorization_servers': ['http://other']})

    def test_rejects_wrong_discovered_issuer(self):
        with self.assertRaises(ValueError):
            self.run_discovery(metadata={**METADATA, 'issuer': ISSUER + '/wrong'})

    def test_requires_pkce(self):
        with self.assertRaises(ValueError):
            self.run_discovery(metadata={**METADATA, 'code_challenge_methods_supported': ['plain']})

    def test_rejects_malformed_pkce_metadata(self):
        for methods in (None, "S256", {}):
            with self.subTest(methods=methods), self.assertRaises(ValueError):
                self.run_discovery(metadata={**METADATA, 'code_challenge_methods_supported': methods})

    def test_rejects_dot_segments(self):
        for suffix in ('/../other/token', '/%2e%2e/token'):
            with self.subTest(suffix=suffix), self.assertRaises(ValueError):
                client.require_local_url(ISSUER + suffix, ISSUER)

    def test_rejects_external_endpoints(self):
        for field in ('authorization_endpoint', 'token_endpoint', 'jwks_uri'):
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.run_discovery(metadata={**METADATA, field: 'https://other.example/endpoint'})

    def test_rejects_missing_endpoint(self):
        with self.assertRaises(ValueError):
            self.run_discovery(metadata={**METADATA, 'token_endpoint': None})

    def test_requires_challenge(self):
        for challenge in ({}, {'WWW-Authenticate': 'Basic realm="test"'}):
            with self.subTest(challenge=challenge), self.assertRaises(ValueError):
                self.run_discovery(challenge=challenge)

    def test_rejects_untrusted_metadata_before_fetch(self):
        with self.assertRaises(ValueError):
            self.run_discovery(challenge={'WWW-Authenticate': 'Bearer resource_metadata="http://other/metadata"'})

    def test_requires_401(self):
        with self.assertRaises(ValueError):
            self.run_discovery(status=200)

    def test_url_restrictions(self):
        for url in ('http://127.0.0.1:9000/realms/s03-mcp-other/token', ISSUER+'/token#x', ISSUER+'/token?q=x', 'http://user@127.0.0.1:9000/realms/s03-mcp/token'):
            with self.subTest(url=url), self.assertRaises(ValueError):
                client.require_local_url(url, ISSUER)

if __name__ == '__main__':
    unittest.main()
