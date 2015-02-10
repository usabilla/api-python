#!/usr/bin/env python
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

# Usabilla API Python Client

import sys, datetime, hashlib, hmac
import requests
import urllib3.request as urllib


class Credentials:
    def __init__(self, clientkey, secretkey):
        if clientkey == '' or secretkey == '':
            raise GeneralError('Emtpy credentials.', 'The credentials you have entered are invalid.')
        self.clientkey = clientkey
        self.secretkey = secretkey
    def getCredentials(self):
        return {'clientKey':self.clientkey,'secretKey':self.secretkey}

class GeneralError(Exception):
    def __init__(self, type, message):
        self.type = type
        self.message = message

    def __str__(self):
        return "%s (%s)" % (self.type, self.message)

    def __repr__(self):
        return "%s(type=%s)" % (self.__class__.__name__, self.type)


class APIClient(Credentials):


    # set up constants
    method = 'GET'
    host = 'data.usabilla.com'
    hostProtocol = 'https://'
    queryParameters = ''
    # Key derivation functions. See:
    # http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
    
    def sign(self,key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

    def getSignatureKey(self,key, longDate):
        kDate = self.sign(('USBL1' + key).encode('utf-8'), longDate)        
        kSigning = self.sign(kDate, 'usbl1_request')
        return kSigning

    def setQueryParameters(self,parameters):
        self.queryParameters = urllib.urlencode(parameters)

    def getQueryParameters(self):
        return self.queryParameters

    def sendSignedRequest(self, scope):
        if self.clientkey is None or self.secretkey is None:
            raise GeneralError('Invalid Access Key.', 'The Access Key supplied is invalid.')
            sys.exit()
            
        
        # Create a date for headers and the credential string
        t = datetime.datetime.utcnow()
        usbldate = t.strftime('%a, %d %b %Y %H:%M:%S GMT') 
        datestamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope
        longDate = t.strftime('%Y%m%dT%H%M%SZ')  


        #Create canonical URI--the part of the URI from domain to query
        canonical_uri = scope

        #Create the canonical query string. In this example (a GET request),
        canonical_querystring = self.getQueryParameters()

        #Create the canonical headers and signed headers
        canonical_headers = 'date:' + usbldate + '\n' + 'host:' + self.host + '\n'

        #Create the list of signed headers

        signed_headers = 'date;host'

        # Create payload hash (hash of the request body content)
        # requests, the payload is an empty string ("").
        payload_hash = hashlib.sha256('').hexdigest()

        # Step 7: Combine elements to create create canonical request
        canonical_request = self.method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
        
     

        # Match the algorithm to the hashing algorithm you use, either SHA-1 or
        algorithm = 'USBL1-HMAC-SHA256'
        credential_scope = datestamp + '/'  + 'usbl1_request'
        
        
        string_to_sign = algorithm + '\n' +  longDate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request).hexdigest()



        # Create the signing key using the function defined above.
        signing_key = self.getSignatureKey(self.secretkey, datestamp)

        # Sign the string_to_sign using the signing_key
        signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()



        authorization_header = algorithm + ' ' + 'Credential=' + self.clientkey + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
        

        headers = {'date':usbldate, 'Authorization':authorization_header}
        
        # ************* SEND THE REQUEST *************
        request_url = self.host + scope + '?' + canonical_querystring
        
        r = requests.get(self.hostProtocol + request_url, headers=headers)

        if r.status_code != 200: 
            return r
        else: 
            return r.json()


    def getButtons(self, optional = None):
        buttons = self.sendSignedRequest('/live/website/button')
        return buttons

    #default value is '*' encoded as stated by RFC3986
    def getFeedbackItems(self, buttonId = '%2A'):
            
        if buttonId is None or buttonId is '':
            raise GeneralError('invalid id', 'Invalid button ID')
        feedbackItems = self.sendSignedRequest('/live/website/button/' + str(buttonId) + '/feedback')
        return feedbackItems

    def getCampaigns(self, optional = None):
        campaigns = self.sendSignedRequest('/live/website/campaign')
        return campaigns

    def getCampaignResults(self, campaignId):
        if campaignId is None or campaignId is '':
            raise GeneralError('invalid id', 'Invalid campaign ID')
        campaignResults = self.sendSignedRequest('/live/website/campaign/' + str(campaignId) + '/results')
        return campaignResults
        
    def getIteratorDispatcher(self):
        iteratorDispatcher = {'campaigns' : self.getCampaigns,
                              'feedbackItems' : self.getFeedbackItems,
                              'campaignResults' : self.getCampaignResults}
        return iteratorDispatcher
                              
    def itemIterator(self, iterator):
        iteratorDispatcher = self.getIteratorDispatcher()
        hasMore = True
        items = []
        while(hasMore):
            try:
                results = iteratorDispatcher[iterator['type']](iterator['id'])
                hasMore = results['hasMore']
                for item in results['items']:
                    items.append(item)
                self.setQueryParameters({'since' : results['lastTimestamp']})
            except:
                return results
        return items        