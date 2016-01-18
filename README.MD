##Usabilla API - Python Client

[![Build Status](https://travis-ci.org/usabilla/api-python.svg?branch=master)](https://travis-ci.org/usabilla/api-python)

The Usabilla Python client allows users to access data from their Usabilla accounts.
It makes use of the API to request the following products and resources:

###Usabilla for Websites
- Buttons
- Feedback items
- Campaigns
- Campaign results
- Campaign statistics
- In-Page widgets
- In-Page feedback

###Usabilla for Email
  - Buttons
  - Feedback items

###Usabilla for Apps
  - Apps
  - Feedback items 

For more information on resources, authorization and available API calls, please visit out [documentation](https://usabilla.com/api).

Changes in version 1.2
- Added In-Page resource

Changes in version 1.1
Resources are now retrieved by providing the following:
  - A scope
  - A product name
  - A resource type

# Installation:
Requires Python 2.7. (Need Collections.OrderedDict)

```bash
python setup.py install
```

# Usage:
## sample command:
```python
>>> import usabilla as ub
>>> api = ub.APIClient('CLIENT-API-KEY', 'CLIENT-SECRET-KEY')
>>> api.set_query_parameters({'limit' : 1})
>>> buttons = api.get_resource(api.SCOPE_LIVE, api.PRODUCT_WEBSITES,api.RESOURCE_BUTTON)
>>> print buttons
```

## output
```json
{
  "count": 1,
  "items": [
    {
      "_id" : "8d73568ac2be",
      "name" : "My button",
    }
  ],
  "hasMore": true,
  "lastTimestamp": 1421232571909752
}
```

###Iterators:

When working with the <code>limit</code> parameters (default value is **100**) you can request resources using the <code>item_iterator()</code> function.
The API returns data in pages. This function returns a [Generator](https://wiki.python.org/moin/Generators) which
traverses these pages for you and yields each result in the current page before retrieving the next page.

##Example usage:

```python
>>> import usabilla as ub
>>> import json
>>> api = ub.APIClient('CLIENT-API-KEY', 'CLIENT-SECRET-KEY')
>>> api.set_query_parameters({'limit' : 1})
>>> feedbackItems = api.get_resource(api.SCOPE_LIVE, api.PRODUCT_WEBSITES,api.RESOURCE_FEEDBACK,'*',iterate=True)
>>> print json.dumps([item for item in feedbackItems], indent=4)
```

Where <code>id</code> is the button id from which the feedback originates.

## output
```json
{
  "id" : "5499612ec4698839368b4573",
  "userAgent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",    
  "comment" : "A random comment.",    
  "location" : "Amsterdam, Netherlands",
  "date" : "2014-01-15T19:48:06.003Z",
  "custom" : {
      "form_name" : "form1"
  },
  "email" : "dev@usabilla",
  "htmlSnippet" : "<a href=\"#\">An anchor element</a>",    
  "image" : "http://usabilla-feedback-dev.s3.amazonaws.com/5499612ec4698839368b4573/detail",
  "labels" : [ 
      "label 1", 
      "label 2"
  ],  
  "nps" : 10,
  "publicUrl" : "http://usabilla.dev/feedback/item/a5cadaf3febf44393401a4be3ebbbf155d9f8d2c",
  "rating" : 5,    
  "buttonId" : "8d73568ac2be",
  "tags" : [ 
      "interesting", 
      "unattractive"
  ],
  "url" : "http://usabilla.com/member/live/site/8d73568ac2be"
}
```

**Note:** Every response is in json format.
