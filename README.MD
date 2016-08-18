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

# Installation:

Requires Python 2.7

```bash
pip install usabilla-api
```

# Buttons example:
```python
>>> import usabilla as ub
>>> api = ub.APIClient('YOUR-ACCESS-KEY', 'YOUR-SECRET-KEY')
>>> api.set_query_parameters({'limit' : 1})
>>> buttons = api.get_resource(api.SCOPE_LIVE, api.PRODUCT_WEBSITES,api.RESOURCE_BUTTON)
>>> print buttons
```

### Iterators

When working with the <code>limit</code> parameters (default value is **100**) you can request resources using the <code>item_iterator()</code> function.
The API returns data in pages. This function returns a [Generator](https://wiki.python.org/moin/Generators) which
traverses these pages for you and yields each result in the current page before retrieving the next page.

## Feedback example

```python
>>> import usabilla as ub
>>> import json
>>> api = ub.APIClient('CLIENT-API-KEY', 'CLIENT-SECRET-KEY')
>>> api.set_query_parameters({'limit' : 1})
>>> feedbackItems = api.get_resource(api.SCOPE_LIVE, api.PRODUCT_WEBSITES,api.RESOURCE_FEEDBACK,'*',iterate=True)
>>> print json.dumps([item for item in feedbackItems], indent=4)
```

Where <code>id</code> is the button id from which the feedback originates.
