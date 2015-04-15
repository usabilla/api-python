"""Usabilla API Python Client."""

# Copyright (c) 2015 Usabilla.com
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS

import datetime
import hashlib
import hmac
import requests
import urllib3.request as urllib
from collections import OrderedDict


class Credentials(object):

    """An object that holds information about client and secret key."""

    def __init__(self, client_key, secret_key):
        """Initialize a Credentials instance."""
        if client_key == '' or secret_key == '':
            raise GeneralError('Emtpy credentials.', 'The credentials you have entered are invalid.')

        self.client_key = client_key
        self.secret_key = secret_key

    def get_credentials(self):
        """Return the client and secret key."""
        return {'client_key': self.client_key, 'secret_key': self.secret_key}


class GeneralError(Exception):

    """GeneralError API exception."""

    def __init__(self, type, message):
        """Initialize a GeneralError exception."""
        self.type = type
        self.message = message

    def __str__(self):
        """String representation of the exception."""
        return "%s (%s)" % (self.type, self.message)

    def __repr__(self):
        """Representation of the exception."""
        return "%s(type=%s)" % (self.__class__.__name__, self.type)


class APIClient(object):

    """APIClient object.

    For the key derivation functions see:
        http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python

    """

    method = 'GET'
    host = 'data.usabilla.com'
    host_protocol = 'https://'

    def __init__(self, client_key, secret_key):
        """Initialize an APIClient object."""
        self.query_parameters = ''
        self.credentials = Credentials(client_key=client_key, secret_key=secret_key)

    def sign(self, key, msg):
        """Get the digest of the message using the specified key."""
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

    def get_signature_key(self, key, long_date):
        """Get the signature key."""
        k_date = self.sign(('USBL1' + key).encode('utf-8'), long_date)
        k_signing = self.sign(k_date, 'usbl1_request')
        return k_signing

    def set_query_parameters(self, parameters):
        """Set the query parameters.

        :param parameters: A `dict` representing the query parameters to be used for the request.
        :type parameters: dict
        """
        self.query_parameters = urllib.urlencode(OrderedDict(sorted(parameters.items())))

    def get_query_parameters(self):
        """Get the query parameters."""
        return self.query_parameters

    def send_signed_request(self, scope):
        """Send the signed request to the API.

        The process is the following:
            1) Create a canonical request
            2) Create a string to sign
            3) Calculate the signature
            4) Sign the request
            5) Send the request

        :param scope: The resource relative url to query for data.
        :type scope: str

        :returns: A `dict` of the data.
        :rtype: dict
        """
        if self.credentials.client_key is None or self.credentials.secret_key is None:
            raise GeneralError('Invalid Access Key.', 'The Access Key supplied is invalid.')

        # Create a date for headers and the credential string.
        t = datetime.datetime.utcnow()
        usbldate = t.strftime('%a, %d %b %Y %H:%M:%S GMT')
        datestamp = t.strftime('%Y%m%d')  # Date w/o time, used in credential scope
        long_date = t.strftime('%Y%m%dT%H%M%SZ')

        # Create canonical URI--the part of the URI from domain to query.
        canonical_uri = scope

        # Create the canonical query string.
        canonical_querystring = self.get_query_parameters()
        
        # Create the canonical headers and signed headers.
        canonical_headers = 'date:' + usbldate + '\n' + 'host:' + self.host + '\n'

        # Create the list of signed headers.
        signed_headers = 'date;host'

        # Create payload hash (hash of the request body content).
        payload_hash = hashlib.sha256('').hexdigest()

        # Combine elements to create canonical request.
        canonical_request = '{method}\n{uri}\n{query}\n{can_headers}\n{signed_headers}\n{hash}'.format(
            method=self.method,
            uri=canonical_uri,
            query=canonical_querystring,
            can_headers=canonical_headers,
            signed_headers=signed_headers,
            hash=payload_hash
        )

        # Match the algorithm to the hashing algorithm you use
        algorithm = 'USBL1-HMAC-SHA256'
        credential_scope = datestamp + '/' + 'usbl1_request'

        string_to_sign = '{algorithm}\n{long_date}\n{credential_scope}\n{digest}'.format(
            algorithm=algorithm,
            long_date=long_date,
            credential_scope=credential_scope,
            digest=hashlib.sha256(canonical_request).hexdigest(),
        )

        # Create the signing key.
        signing_key = self.get_signature_key(self.credentials.secret_key, datestamp)

        # Sign the string_to_sign using the signing_key.
        signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

        # Constrcut the authorization header.
        authorization_header = (
            '{algorithm} Credential={cred}/{cred_scope}, SignedHeaders={signed_headers}, Signature={signature}'
        ).format(
            algorithm=algorithm,
            cred=self.credentials.client_key,
            cred_scope=credential_scope,
            signed_headers=signed_headers,
            signature=signature,
        )

        headers = {'date': usbldate, 'Authorization': authorization_header}

        # Send the request.
        request_url = self.host + scope + '?' + canonical_querystring

        r = requests.get(self.host_protocol + request_url, headers=headers)
        
        if r.status_code != 200:
            return r
        else:
            return r.json()

    def get_buttons(self, optional=None):
        """Send request to get button data."""
        buttons = self.send_signed_request('/live/website/button')
        return buttons

    def get_feedback_items(self, button_id='%2A'):
        """Send request to get data for feedback items.

        :param button_id: The button id. Default value is '*' encoded as stated by RFC3986.
        :type button_id: str
        """
        if button_id is None or button_id is '':
            raise GeneralError('invalid id', 'Invalid button ID')
        if button_id == '*':
            button_id = '%2A'
            
        feedback_items = self.send_signed_request('/live/website/button/' + str(button_id) + '/feedback')
        return feedback_items

    def get_campaigns(self, optional=None):
        """Send request to get campaign data."""
        campaigns = self.send_signed_request('/live/website/campaign')
        return campaigns

    def get_campaign_results(self, campaign_id):
        """Send request to get campaign result data.

        :param campaign_id: The campaign id.
        :type campaign_id: str
        """
        if campaign_id is None or campaign_id is '':
            raise GeneralError('invalid id', 'Invalid campaign ID')
        campaign_results = self.send_signed_request('/live/website/campaign/' + str(campaign_id) + '/results')
        return campaign_results

    def item_iterator(self, resource_group, resource_id):
        """Get items using an iterator.

        :param resource_group: A `string` that specifies the type of resources we want to iterate over iterator
        :param resource_id: the id of the resource.

        :type resource_group: str
        :type resource_id: str

        :returns: An `iterator` that yeilds the requested data.
        :rtype: iterator
        """
        item_retriever = self._get_iterator_function(resource_group)
        if item_retriever is None:
            message = 'Cannot create iterator for resource group {}. Unknown group.'.format(resource_group)
            raise GeneralError('No iterator for resource group', message)

        has_more = True
        while has_more:
            try:
                results = item_retriever(resource_id)
                has_more = results['hasMore']
                for item in results['items']:
                    yield item
                self.set_query_parameters({'since': results['lastTimestamp']})
            except GeneralError, requests.HTTPError:
                pass

    def _get_iterator_function(self, resource_group):
        """Get the item retriever for iterating through the resource_group."""
        return {
            'campaigns': self.get_campaigns,
            'feedback_items': self.get_feedback_items,
            'campaign_results': self.get_campaign_results,
        }.get(resource_group, None)

