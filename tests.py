"""Unit tests for the Usabilla API."""

import sys
import unittest
import usabilla as ub

from unittest import TestCase, main as unittest_main


class TestCredentials(TestCase):

    def setUp(self):
        self.client_key = 'ACCESS-KEY'
        self.secret_key = 'SECRET-KEY'

    def test_credentials(self):
        credentials = ub.Credentials(self.client_key, self.secret_key)
        self.assertIsInstance(credentials, ub.Credentials)

    def test_get_credentials(self):
        credentials = ub.Credentials(self.client_key, self.secret_key)
        client_credentials = credentials.get_credentials()
        client_key = client_credentials['client_key']
        secret_key = client_credentials['secret_key']
        self.assertEqual(self.client_key, client_key)
        self.assertEqual(self.secret_key, secret_key)

    def test_empty_credentials_exception(self):
        with self.assertRaises(Exception):
            ub.Credentials()
            ub.Credentials('1')
        with self.assertRaises(ub.GeneralError):
            ub.Credentials(None, '1')
            ub.Credentials('', 2)
            ub.Credentials('', '')
            ub.Credentials(2, '')


class TestClient(TestCase):

    def setUp(self):
        self.client_key = 'ACCESS-KEY'
        self.secret_key = 'SECRET-KEY'
        credentials = ub.Credentials(self.client_key, self.secret_key)
        self.client = ub.APIClient(ub.APIClient, credentials)
        self.assertIsInstance(self.client, ub.APIClient)

    def test_client_constants(self):
        self.assertEqual(self.client.method, 'GET')
        self.assertEqual(self.client.host, 'data.usabilla.com')
        self.assertEqual(self.client.hostProtocol, 'https://')
        self.assertEqual(self.client.queryParameters, '')

    @unittest.skipIf(sys.version_info > (2, 7), "signature assertion not supported for this version")
    def test_sign_key(self):
        signed_key = self.client.sign(self.secret_key, 'usbl1_request')
        self.assertEqual(signed_key, '&-\x88\x80Z9\xe8Pnvx\xe4S\xeeZ\x9fG\xc5\xf7g\x11|\xc1\xaa~q(\xef\xaf\x95\xc0\xac')

    @unittest.skipIf(sys.version_info > (2, 7), "signature assertion not supported for this version")
    def test_get_signature_key(self):
        datestamp = '20150115'
        signing_key = self.client.getSignatureKey(self.secret_key, datestamp)
        self.assertEqual(
            signing_key, '\x15\x8d\xd7U\xceG\xdeH\x8aHwU\xf5qg\xae\xd4Z\x19`\xedM\x80\x87\x97V\xbf\xe9pw\xaa\xae')

    @unittest.skipIf(sys.version_info > (2, 7), "query parameter order different for urllib3.")
    def test_query_parameters(self):
        params = {'limit': 1}
        self.client.setQueryParameters(params)
        self.assertEqual(self.client.queryParameters, 'limit=1')
        params = {'limit': 1, 'since': 1235454}
        self.client.setQueryParameters(params)
        self.assertEqual(self.client.queryParameters, 'since=1235454&limit=1')
        params = ub.urllib.urlencode(params)
        self.assertEqual(self.client.getQueryParameters(), params)


if __name__ == '__main__':
    unittest_main()
