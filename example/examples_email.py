"""Example getting button data."""

import pprint
import usabilla as ub

if __name__ == '__main__':
    # Create an API client with client and secret keys
    api = ub.APIClient('YOUR-ACCESS-KEY', 'YOUR-SECRET-KEY')

    # Set the limit of buttons to retrieve to 1
    api.set_query_parameters({'limit': 1})

    # Get the buttons
    buttons = api.get_resource(api.SCOPE_LIVE, api.PRODUCT_WEBSITES, api.RESOURCE_BUTTON)

    pprint.PrettyPrinter(indent=4).pprint(buttons)



// Get all email widgets for this account.
api.email.widgets.get().then((emailWidgets) => {

  // Get the feedback for a email widget with id.
  var emailQuery = {
    id: emailWidgets[0].id
  };

  // Get the feedback of the first email widget
  api.email.widgets.feedback.get(emailQuery).then((feedback) => {
    console.log('# email feedback', feedback.length);
  });
});

// Get all apps forms for this account.
api.apps.forms.get().then((appsForms) => {

  // Get the feedback for a apps form with id.
  var appsQuery = {
    id: appsForms[1].id
  };

  // Get the feedback of the second app form
  api.apps.forms.feedback.get(appsQuery).then((feedback) => {
    console.log('# apps feedback', feedback.length);
  });
});