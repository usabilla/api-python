"""Example using the feedbback iterator."""

import pprint
import usabilla as ub

if __name__ == '__main__':
    # Create an API client with client and secret keys
    api = ub.APIClient('YOUR-ACCESS-KEY', 'YOUR-SECRET-KEY')

    # Set the limit of feedback items to retrieve to 1
    api.set_query_parameters({'limit': 1})

    # Get the feedback items for a specific button
    feedback_items = api.get_resource(api.SCOPE_LIVE, api.PRODUCT_WEBSITES,api.RESOURCE_FEEDBACK,'BUTTON-ID',iterate=True)

    pprint.PrettyPrinter(indent=4).pprint([item for item in feedback_items])
