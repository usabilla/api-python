##Usabilla API - Python Client

[![Build Status](https://travis-ci.org/usabilla/api-python.svg?branch=master)](https://travis-ci.org/usabilla/api-python)

The Usabilla Python client allows users to access data from their Usabilla accounts.
It makes use of the API to request the following resource items:

	- Buttons
	- Feedback items
	- Campaign
	- Campaign results

For more information on resources, authorization and available API calls, please visit out [documentation](https://usabilla.com/api).


# Installation:
Requires Python 2.7. (Need Collections.OrderedDict)

```bash
python setup.py install
```

# Usage:
## sample command:
```python
>>> import usabilla as ub
>>> clientApi = ub.APIClient('CLIENT-API-KEY', 'CLIENT-SECRET-KEY')
>>> clientApi.setQueryParameters({'limit' : 1})
>>> buttons = clientApi.getButtons()
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

When working with the <code>limit</code> parameters (default value is **100**) you can request resources using the <code>itemIterator()</code> function.
Using the <code>hasMore</code> flag it will request items until the value of the flag is **False**.

##Example usage:

```python
>>> import usabilla as ub
>>> clientApi = ub.APIClient('CLIENT-API-KEY', 'CLIENT-SECRET-KEY')
>>> clientApi.setQueryParameters({'limit' : 1})
>>> feedbackItems = clientApi.itemIterator({'type':'feedbackItems', 'id' : '8d73568ac2be'})
>>> print feedbackItems
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
