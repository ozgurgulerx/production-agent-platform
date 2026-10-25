import unittest
from urllib.parse import parse_qs, urlencode, urlsplit
from unittest.mock import patch
import oauth_client as client

class LoginTests(unittest.TestCase):
    def callback(self, **updates):
        return '/callback?' + urlencode({'code': 'example-code', 'state': 'expected', 'iss': client.EXPECTED_ISSUER, **updates})

    def test_pkce_rfc7636_vector(self):
        self.assertEqual(client.pkce_challenge('dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk'), 'E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM')

    def test_authorization_parameters(self):
        url = client.authorization_url({'authorization_endpoint': client.EXPECTED_ISSUER + '/protocol/openid-connect/auth'}, 'verifier', 'state', 'ayse')
        query = parse_qs(urlsplit(url).query)
        self.assertEqual(query['resource'], [client.MCP_URL])
        self.assertEqual(query['code_challenge_method'], ['S256'])
        self.assertEqual(query['redirect_uri'], [client.REDIRECT_URI])
        self.assertEqual(query['prompt'], ['login'])
        self.assertNotIn('verifier', url)

    def test_callback_accepts_valid_response(self):
        self.assertEqual(client.validate_callback(self.callback(), 'expected'), 'example-code')

    def test_callback_rejects_invalid_responses(self):
        paths = [self.callback(state='wrong'), self.callback(iss='http://wrong'), self.callback(code=''), self.callback() + '&code=duplicate', self.callback().replace('/callback?', '/wrong?'), '/callback?code=x&state=expected', self.callback() + '&error=access_denied']
        for path in paths:
            with self.subTest(path=path), self.assertRaises(ValueError):
                client.validate_callback(path, 'expected')

    def test_denial_is_explicit(self):
        with self.assertRaises(client.LoginDenied):
            client.validate_callback('/callback?' + urlencode({'error':'access_denied','state':'expected','iss':client.EXPECTED_ISSUER}), 'expected')

    def test_exchange_uses_same_resource_and_verifier(self):
        response = {'access_token':'test-only', 'token_type':'Bearer','scope':'tickets.read'}
        with patch.object(client, 'request_json', return_value=(200, {}, response)) as request:
            self.assertEqual(client.exchange_code({'token_endpoint':client.EXPECTED_ISSUER+'/protocol/openid-connect/token'}, 'code', 'verifier'), response)
        self.assertEqual(request.call_args.kwargs['form']['resource'], client.MCP_URL)
        self.assertEqual(request.call_args.kwargs['form']['code_verifier'], 'verifier')
        self.assertNotIn('client_secret', request.call_args.kwargs['form'])

    def test_exchange_rejects_invalid_token_response(self):
        for response in ({}, {'access_token':'x','token_type':'Other'}, {'access_token':'','token_type':'Bearer'}):
            with self.subTest(response=response), patch.object(client, 'request_json', return_value=(200, {}, response)), self.assertRaises(ValueError):
                client.exchange_code({'token_endpoint':client.EXPECTED_ISSUER+'/token'}, 'code', 'verifier')

    def test_summary_never_contains_tokens(self):
        result = client.token_summary({'access_token':'secret','refresh_token':'secret','id_token':'secret','scope':'tickets.read','token_type':'Bearer','expires_in':300})
        self.assertEqual(set(result), {'token_received','token_type','scope','expires_in'})
        self.assertNotIn('secret', str(result))

    def test_login_orchestration_keeps_verifier_for_exchange(self):
        with patch.object(client.secrets, 'token_urlsafe', side_effect=['verifier','state']), patch.object(client, 'receive_code', return_value='code') as callback, patch.object(client, 'exchange_code', return_value={'access_token':'test-only'}) as exchange:
            metadata = {'authorization_endpoint':client.EXPECTED_ISSUER+'/auth'}
            client.login(metadata, 'ayse')
            exchange.assert_called_once_with(metadata, 'code', 'verifier')
            self.assertEqual(callback.call_args.args[1], 'state')

    def test_exchange_401_rejected(self):
        with patch.object(client, 'request_json', return_value=(401, {}, {})), self.assertRaises(ValueError):
            client.exchange_code({'token_endpoint':client.EXPECTED_ISSUER+'/token'}, 'code', 'verifier')

    def test_callback_listener_validates_and_closes(self):
        from urllib.request import Request, urlopen
        from urllib.error import HTTPError
        import threading
        received = []
        failures = []
        def browser(*args, **kwargs):
            def send():
                try:
                    for target in (self.callback(state='wrong'), self.callback()):
                        try:
                            with urlopen('http://127.0.0.1:8765' + target, timeout=5) as response:
                                received.append(response.status)
                        except HTTPError as error:
                            received.append(error.code)
                except Exception as error:
                    failures.append(error)
            thread = threading.Thread(target=send)
            thread.start()
            threads.append(thread)
        threads = []
        with patch.object(client.subprocess, 'run', side_effect=browser):
            self.assertEqual(client.receive_code('http://example.invalid', 'expected', timeout=10), 'example-code')
        for thread in threads:
            thread.join(5)
        self.assertEqual(failures, [])
        self.assertEqual(received, [400, 200])

    def test_listener_timeout_closes_socket(self):
        with patch.object(client.subprocess, 'run'), self.assertRaises(TimeoutError):
            client.receive_code('http://example.invalid', 'expected', timeout=0)

    def test_http_reader_posts_form_without_following_redirects(self):
        import io
        from unittest.mock import MagicMock
        response = MagicMock()
        response.__enter__.return_value = response
        response.status = 200
        response.read.return_value = b'{"access_token":"test-only"}'
        with patch.object(client, 'build_opener') as opener:
            opener.return_value.open.return_value = response
            result = client.request_json('http://127.0.0.1:9000/token', form={'code':'test-code'})
        request = opener.return_value.open.call_args.args[0]
        self.assertEqual(request.get_method(), 'POST')
        self.assertEqual(request.data, b'code=test-code')
        self.assertEqual(result[0], 200)
        self.assertIsNone(client.NoRedirects().redirect_request(None,None,302,'',{},'http://elsewhere'))

    def test_http_reader_rejects_invalid_responses(self):
        from unittest.mock import MagicMock
        for status, raw in ((302,b'{}'), (200,b'[]'), (200,b'x'*1048577)):
            response = MagicMock()
            response.__enter__.return_value = response
            response.status = status
            response.read.return_value = raw
            with patch.object(client, 'build_opener') as opener, self.assertRaises(ValueError):
                opener.return_value.open.return_value = response
                client.request_json('http://127.0.0.1:9000/example')

    def test_main_prints_only_summary(self):
        import io
        with patch('sys.argv', ['oauth_client.py','--login']), patch.object(client,'discover',return_value={}), patch.object(client,'login',return_value={'access_token':'hidden','scope':'tickets.read'}), patch('sys.stdout',new_callable=io.StringIO) as output:
            client.main()
        self.assertNotIn('hidden', output.getvalue())
        self.assertIn('token_received', output.getvalue())

if __name__ == '__main__':
    unittest.main()
