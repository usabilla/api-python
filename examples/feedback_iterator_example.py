"""Example using the feedbback iterator."""

import pprint
import usabilla as ub

if __name__ == '__main__':
    # Create an API client with client and secret keys
    client_api = ub.APIClient('CLIENT-API-KEY', 'CLIENT-SECRET-KEY')

    # Set the limit of feedback items to retrieve to 1
    client_api.set_query_parameters({'limit': 1})

    # Get the feedback items for a specific button
    feedback_items = client_api.item_iterator('feedback_items', 'BUTTON-ID')

    pprint.PrettyPrinter(indent=4).pprint([item for item in feedback_items])
