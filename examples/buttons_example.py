"""Example getting button data."""

import pprint
import usabilla as ub

if __name__ == '__main__':
    # Create an API client with client and secret keys
    api = ub.APIClient('YOUR-ACCESS-KEY', 'YOUR-SECRET-KEY')

    # Set the limit of buttons to retrieve to 1
    api.set_query_parameters({'limit': 1})

    # Get the buttons
    buttons = api.get_resource(api.SCOPE_LIVE, api.PRODUCT_WEBSITES,api.RESOURCE_BUTTON)

    pprint.PrettyPrinter(indent=4).pprint(buttons)
