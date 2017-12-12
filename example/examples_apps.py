"""Example Usabilla for Apps"""

import usabilla as ub

from datetime import datetime, timedelta

if __name__ == '__main__':
    # Create an API client with access key and secret key
    api = ub.APIClient('YOUR-ACCESS-KEY', 'YOUR-SECRET-KEY')

    # Set the limit of buttons to retrieve to 1
    if False:
        api.set_query_parameters({'limit': 1})

    # Set a limit for last 7 days
    if False:
        epoch = datetime(1970, 1, 1)
        since = timedelta(days=7)
        since_unix = (datetime.utcnow() - since - epoch).total_seconds() * 1000
        api.set_query_parameters({'since': since_unix})

    # Get all apps forms for this account
    forms = api.get_resource(api.SCOPE_LIVE, api.PRODUCT_APPS, api.RESOURCE_APP)
    first_form = forms['items'][0]
    print first_form['name']

    # Get the feedback of the first app form
    feedback = api.get_resource(
        api.SCOPE_LIVE,
        api.PRODUCT_APPS,
        api.RESOURCE_FEEDBACK,
        first_form['id'],
        iterate=True)
    print len([item for item in feedback])

    # Campaigns for apps
    app_campaigns = api.get_resource(
        api.SCOPE_LIVE,
        api.PRODUCT_APPS,
        api.RESOURCE_CAMPAIGN)
    first_campaign = app_campaigns['items'][0]
    responses = api.get_resource(
        api.SCOPE_LIVE,
        api.PRODUCT_APPS,
        api.RESOURCE_CAMPAIGN_RESULT,
        first_campaign['id'],
        iterate=True)
    print len([item for item in responses])
