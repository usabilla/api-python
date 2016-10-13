"""Examples Usabilla for Websites"""

import pprint
import usabilla as ub

if __name__ == '__main__':
    # Create an API client with access key and secret key
    api = ub.APIClient('YOUR-ACCESS-KEY', 'YOUR-SECRET-KEY')

	# Get all buttons for this account
    buttons = api.get_resource(api.SCOPE_LIVE, api.PRODUCT_WEBSITES,api.RESOURCE_BUTTON)
    first_button = buttons['items'][0]
    print first_button['name']

    # Get the feedback items for the first button of the list
    feedback_items = api.get_resource(api.SCOPE_LIVE, api.PRODUCT_WEBSITES, api.RESOURCE_FEEDBACK, first_button['id'], iterate=True)
    print len([item for item in feedback_items])

    # ---------------------------------------
	# Get all campaigns for this account
    campaigns = api.get_resource(api.SCOPE_LIVE, api.PRODUCT_WEBSITES, api.RESOURCE_CAMPAIGN)
    first_campaign = campaigns['items'][0]
    print first_campaign['name']

    # Get the responses of the first campaign
    responses = api.get_resource(api.SCOPE_LIVE, api.PRODUCT_WEBSITES, api.RESOURCE_CAMPAIGN_RESULT, first_campaign['id'], iterate=True)
    print len([item for item in responses])

    # Get the stats of the first campaign
    stats = api.get_resource(api.SCOPE_LIVE, api.PRODUCT_WEBSITES, api.RESOURCE_CAMPAIGN_STATS, first_campaign['id'])
    print stats


    # ---------------------------------------
    # in-page is not yet available