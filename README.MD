# Usabilla API - Python Client

[![Build Status](https://travis-ci.org/usabilla/api-python.svg?branch=master)](https://travis-ci.org/usabilla/api-python)
[![PyPI version](https://badge.fury.io/py/usabilla-api.svg)](https://badge.fury.io/py/usabilla-api)
[![Coverage Status](https://coveralls.io/repos/github/usabilla/api-python/badge.svg?branch=master)](https://coveralls.io/github/usabilla/api-python?branch=master)

The Usabilla Python client allows users to access data from their Usabilla accounts.
It makes use of the API to request the following products and resources:

### Usabilla for Websites

- Buttons
- Feedback items
- Campaigns
- Campaign results
- Campaign statistics
- In-Page widgets
- In-Page feedback

### Usabilla for Email

- Buttons
- Feedback items

### Usabilla for Apps

- Apps
- Feedback items
- Campaigns
- Campaign results

For more information on resources, authorization and available API calls, please visit our [documentation](https://developers.usabilla.com).

## Installation:

Requires Python 3. 
Support for Python 2.7 is expected but not tested or validated.

```bash
pip install usabilla-api
```

## Examples

The example folder contains an  example of the client, which gives an idea how the client can be used and what is possible.

### Iterators

When working with the <code>limit</code> parameters (default value is **100**) you can request resources using the <code>item_iterator()</code> function.
The API returns data in pages. This function returns a [Generator](https://wiki.python.org/moin/Generators) which
traverses these pages for you and yields each result in the current page before retrieving the next page.

## Support

The Usabilla Python Client API is maintained by Usabilla Development Team. Everyone is encouraged to file bug reports, feature requests, and pull requests through GitHub. This input is critical and will be carefully considered, but we can’t promise a specific resolution or time frame for any request. For more information please email our Support Team at support@usabilla.com.

## Releasing [internal]

In order to release a new version of this library, follow these steps:
- bump version in setup.py
- merge and tag the new release with `v<versio>`
- run `python -m build`
- upload release to pypi-test: `python -m twine upload --repository testpypi dist/*`
- upload release to pypi: `python -m twine upload --repository pypi dist/*`