# RFID Authentication

This system is designed to be very simple to implement. If your device can craft an HTTP request and parse the response, it can authenticate an RFID tag against the member database.

# Use

To check a tag, simply request:

    https://members.pumpingstationone.org/rfid/check/<resource>/<tag>

Valid resources are stored in the member's site Django admin interface - in 'Resources.'

To query a tag for the front door (which all members can open):

    https://members.pumpingstationone.org/rfid/check/FrontDoor/123412341234

The tag value should be 12 hex characters. If the tag is valid (assigned to a member's account on the site) the server will return 

    Yes

and if the tag is not valid, the server will return

    No

Easy peasy.
