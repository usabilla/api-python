import logging
from unittest.mock import call
import requests
import usabilla as ub

from mock import Mock
from unittest import TestCase, main as unittest_main


logging.basicConfig(level=logging.DEBUG)


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


class TestGeneralError(TestCase):

    def setUp(self):
        self.error = ub.GeneralError('type', 'message')

    def test_str(self):
        self.assertEqual(str(self.error), 'type (message)')

    def test_repr(self):
        self.assertEqual(repr(self.error), 'GeneralError(type=type)')


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
        self.assertEqual(self.client.host_protocol, 'https://')
        self.assertEqual('', self.client.query_parameters)

    def test_sign_key(self):
        signed_key = self.client.sign(self.secret_key.encode('utf-8'), 'usbl1_request'.encode('utf-8'))
        self.assertEqual(
            signed_key,  b"&-\x88\x80Z9\xe8Pnvx\xe4S\xeeZ\x9fG\xc5\xf7g\x11|\xc1\xaa~q(\xef\xaf\x95\xc0\xac")

    def test_get_signature_key(self):
        datestamp = '20150115'
        signing_key = self.client.get_signature_key(self.secret_key, datestamp)
        self.assertEqual(
            signing_key, b"\x15\x8d\xd7U\xceG\xdeH\x8aHwU\xf5qg\xae\xd4Z\x19`\xedM\x80\x87\x97V\xbf\xe9pw\xaa\xae")

    def test_query_parameters(self):
        params = {'limit': 1}
        self.client.set_query_parameters(params)
        self.assertEqual(self.client.get_query_parameters(), 'limit=1')
        params = {'limit': 1, 'since': 1235454}
        self.client.set_query_parameters(params)
        self.assertEqual(self.client.get_query_parameters(), 'limit=1&since=1235454')

    def test_check_resource_validity(self):
        with self.assertRaises(ub.GeneralError):
            self.client.check_resource_validity(
                'nonexisting',
                'nonexisting',
                'nonexisting')
        with self.assertRaises(ub.GeneralError):
            self.client.check_resource_validity(
                'live',
                'nonexisting',
                'nonexisting')
        with self.assertRaises(ub.GeneralError):
            self.client.check_resource_validity(
                'live',
                'websites',
                'nonexisting')
        self.assertEqual(
            self.client.check_resource_validity('live', 'websites', 'button'),
            '/live/websites/button')
        self.assertEqual(
            self.client.check_resource_validity('live', 'apps', 'campaign'),
            '/live/apps/campaign')
        self.assertEqual(
            self.client.check_resource_validity(
                'live',
                'apps',
                'campaign_result'),
            '/live/apps/campaign/:id/results')

    def test_handle_id(self):
        url = '/live/websites/button/:id/feedback'
        with self.assertRaises(ub.GeneralError):
            self.client.handle_id(url, '')
        self.assertEqual(self.client.handle_id(url, '*'), '/live/websites/button/%2A/feedback')
        self.assertEqual(self.client.handle_id(url, 42), '/live/websites/button/42/feedback')

    def test_item_iterator(self):
        items = ['one', 'two', 'three', 'four']
        has_more = {'hasMore': True, 'items': items[:2], 'lastTimestamp': 1400000000001}
        no_more = {'hasMore': False, 'items': items[2:], 'lastTimestamp': 1400000000002}
        expected_set_query_parameters_calls = [ call({'since': 1400000000001}), call({'since': 1400000000002}), call({}) ]

        self.client.set_query_parameters = Mock()
        self.client.send_signed_request = Mock(side_effect=[has_more, no_more])

        index = 0
        for item in self.client.item_iterator('/some/url'):
            self.assertEqual(item, items[index])
            index += 1

        self.assertEqual(self.client.set_query_parameters.call_args_list, expected_set_query_parameters_calls)
        self.assertEqual(self.client.send_signed_request.call_count, 2)

        self.client.send_signed_request.side_effect = requests.exceptions.HTTPError('mocked error')
        with self.assertRaises(requests.exceptions.HTTPError):
            list(self.client.item_iterator('/some/url'))

    def test_item_iterator_resets_query_parameters_after_returning_all_items(self):
        first_response = {'hasMore': True, 'items': [1], 'lastTimestamp': 1400000000001}
        second_response = {'hasMore': False, 'items': [2], 'lastTimestamp': 1400000000002}
        third_response = {'hasMore': False, 'items': [3], 'lastTimestamp': 1400000000003}

        self.client.send_signed_request = Mock(side_effect=[first_response, second_response, third_response])

        expected_query_parameters = ['', 'since=1400000000001', '']

        index = 0
        for response in [self.client.item_iterator('/some/url'), self.client.item_iterator('/some/url')]:
            for _ in response:
                self.assertEqual(expected_query_parameters[index], self.client.get_query_parameters())
                index+=1

        self.assertEqual(self.client.send_signed_request.call_count, 3)

    def test_get_resource(self):
        self.client.item_iterator = Mock()
        self.client.send_signed_request = Mock()
        self.client.get_resource('live', 'websites', 'feedback', 42)
        self.client.send_signed_request.assert_called_with('/live/websites/button/42/feedback')
        self.client.get_resource('live', 'websites', 'button', None, True)
        self.client.item_iterator.assert_called_with('/live/websites/button')


if __name__ == '__main__':
    unittest_main()
