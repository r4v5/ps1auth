#!/usr/bin/env python
from django.conf import settings
import urllib2
import json
from django.core.cache import cache

class ZohoClient(object):
    """ work in progress, Builds up a list of zoho users """
    api_key = settings.ZOHO_AUTHTOKEN

    def get_contacts(self):
        json_contacts = cache.get("zoho_contacts")
        if json_contacts == None:
            print("fetching records")
            url = ("https://crm.zoho.com/crm/private/json/Contacts/getRecords?" 
                  "authtoken={0}&scope=crmapi".format(self.api_key))
            result = urllib2.urlopen(url)
            raw_output = result.read()
            json_contacts = json.loads(raw_output)
            cache.set("zoho_contacts", json_contacts)
        return json_contacts

if __name__ == '__main__':
    from pprint import pprint
    zc = ZohoClient()
    pprintzc.get_contacts()
    zc.get_contacts()

