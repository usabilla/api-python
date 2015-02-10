from unittest import TestCase, main as unittest_main
import usabilla as ub
import sys, unittest


class TestCredentials(TestCase):

    def setUp(self):
        self.accessKey = 'ACCESS-KEY'
        self.secretKey = 'SECRET-KEY'

    def testCredentialsObject(self):
        credentialObj = ub.Credentials(self.accessKey, self.secretKey)
        self.assertIsInstance(credentialObj, ub.Credentials)

    def testGetCredentials(self):
        credentialObj = ub.Credentials(self.accessKey, self.secretKey)
        clientCredentials = credentialObj.getCredentials()
        accessKey = clientCredentials['clientKey']
        secretKey = clientCredentials['secretKey']
        self.assertEqual(self.accessKey, accessKey)
        self.assertEqual(self.secretKey, secretKey)

    def testEmptyCredentialsException(self):
        with self.assertRaises(Exception):
            ub.Credentials()
            ub.Credentials('1')
        with self.assertRaises(ub.GeneralError):
            ub.Credentials(None,'1')
            ub.Credentials('',2)
            ub.Credentials('','')
            ub.Credentials(2,'')


class TestClient(TestCase):

    def setUp(self):
        self.accessKey = 'ACCESS-KEY'
        self.secretKey = 'SECRET-KEY'
        credentialObj = ub.Credentials(self.accessKey, self.secretKey)
        self.client = ub.APIClient(ub.APIClient,credentialObj)
        self.assertIsInstance(self.client, ub.APIClient)

    def testClientConstants(self):
        self.assertEqual(self.client.method, 'GET')
        self.assertEqual(self.client.host, 'data.usabilla.com')
        self.assertEqual(self.client.hostProtocol, 'https://')
        self.assertEqual(self.client.queryParameters, '')

    @unittest.skipIf(sys.version_info > (2, 7),
         "signature assertion not supported for this version")
    def testSignKey(self):
        signedKey = self.client.sign(self.secretKey,'usbl1_request')
        self.assertEqual(signedKey, '&-\x88\x80Z9\xe8Pnvx\xe4S\xeeZ\x9fG\xc5\xf7g\x11|\xc1\xaa~q(\xef\xaf\x95\xc0\xac')

    @unittest.skipIf(sys.version_info > (2, 7),
         "signature assertion not supported for this version")
    def testGetSignatureKey(self):
        datestamp = '20150115'
        signing_key = self.client.getSignatureKey(self.secretKey, datestamp)
        self.assertEqual(signing_key, '\x15\x8d\xd7U\xceG\xdeH\x8aHwU\xf5qg\xae\xd4Z\x19`\xedM\x80\x87\x97V\xbf\xe9pw\xaa\xae')

    @unittest.skipIf(sys.version_info > (2, 7),
         "query parameter order different for urllib3.")
    def testQueryParameters(self):
        params = {'limit':1}
        self.client.setQueryParameters(params)
        self.assertEqual(self.client.queryParameters, 'limit=1')
        params = {'limit':1, 'since':1235454}
        self.client.setQueryParameters(params)
        self.assertEqual(self.client.queryParameters, 'since=1235454&limit=1')
        params = ub.urllib.urlencode(params)
        self.assertEqual(self.client.getQueryParameters(), params)


if __name__ == '__main__':
    unittest_main()
