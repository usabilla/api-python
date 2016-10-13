"""Example Usabilla for Email"""

import usabilla as ub

if __name__ == '__main__':
    # Create an API client with access key and secret key
    api = ub.APIClient('YOUR-ACCESS-KEY', 'YOUR-SECRET-KEY')

    # Get all email widgets for this account
    widgets = api.get_resource(api.SCOPE_LIVE, api.PRODUCT_EMAIL, api.RESOURCE_BUTTON)
    first_widget = widgets['items'][0]
    print first_widget['name']

    # Get the feedback of the first email widget
    feedback = api.get_resource(api.SCOPE_LIVE, api.PRODUCT_EMAIL, api.RESOURCE_FEEDBACK, first_widget['id'], iterate=True)
    print len([item for item in feedback])
