"""Example getting button data."""

import pprint
import usabilla as ub

if __name__ == '__main__':
    # Create an API client with client and secret keys
    client_api = ub.APIClient('CLIENT-API-KEY', 'CLIENT-SECRET-KEY')

    # Set the limit of buttons to retrieve to 1
    client_api.set_query_parameters({'limit': 1})

    # Get the buttons
    buttons = client_api.get_buttons()

    pprint.PrettyPrinter(indent=4).pprint(buttons)
