#!/usr/bin/env python
from django.conf import settings
import urllib2
import json
from django.core.cache import cache
from zoho_integration.models import Contact
from datetime import datetime

class ZohoClient(object):
    """ work in progress, Builds up a list of zoho users """
    api_key = settings.ZOHO_AUTHTOKEN

    def get_contacts(self, most_recent='1970-01-01%2012:00:00'):
        print("fetching records")
        url = ("https://crm.zoho.com/crm/private/json/Contacts/getRecords?" 
                "authtoken={0}&scope=crmapi&lastModifiedTime={1}&"
                "sortOrderString=asc&sortColumnString=Modified%20Time".format(self.api_key, most_recent))
        json_contacts = cache.get(url)
        if not json_contacts:
            print("downloading new info")
            result = urllib2.urlopen(url)
            raw_output = result.read()
            json_contacts = json.loads(raw_output)
            cache.set(url, json_contacts)
        entries = json_contacts[u'response'][u'result'][u'Contacts'][u'row']
        sane_contacts = []
        for entry in entries:
            e = entry[u'FL']
            sane_contact = dict(map(lambda x: (x['val'], x['content']), e))
            sane_contacts.append(sane_contact)
        return sane_contacts

if __name__ == '__main__':
    from pprint import pprint
    try:
        latest = Contact.objects.latest('modified_time')
    except Contact.DoesNotExist:
        latest = "1970-01-01%2012:00:00"
    pprint(latest)
    zc = ZohoClient()
    contacts = zc.get_contacts(latest)
    for contact in contacts:
        if u'Membership Status' in contact:
            pprint(contact)
            c = Contact()
            c.contact_id = contact[u'CONTACTID']
            c.first_name = contact[u'First Name']
            c.last_name = contact['Last Name']
            c.email = contact[u'Email']
            c.membership_status = contact[u'Membership Status']
            c.modified_time = datetime.strptime(contact[u'Modified Time'], '%Y-%m-%d %H:%M:%S')
            c.save()

    #pprint(zc.get_contacts())

