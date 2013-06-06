#!/usr/bin/env python
from django.conf import settings
import urllib2
import json
from django.core.cache import cache
from zoho_integration.models import Contact
from datetime import datetime
import pytz

class ZohoClient(object):
    """ work in progress, Builds up a list of zoho users """
    api_key = settings.ZOHO_AUTHTOKEN

    def get_contacts(self, most_recent='1970-01-01%2012:00:00'):
        print("fetching records")
        url = ("https://crm.zoho.com/crm/private/json/Contacts/getRecords?" 
                "authtoken={0}&scope=crmapi&lastModifiedTime={1}&fromIndex=1&toIndex=200&"
                "sortOrderString=asc&sortColumnString=Modified%20Time".format(self.api_key, most_recent))
        response = cache.get(url)
        if not response:
            result = urllib2.urlopen(url)
            raw_output = result.read()
            response = json.loads(raw_output)
            if not u'result' in response[u'response']:
                return []
            cache.set(url, response)
        entries = response[u'response'][u'result'][u'Contacts'][u'row']
        sane_contacts = []

        # zoho returns a list if there is more than one result, but just the
        # one result if there is only one result
        if isinstance(entries, list):
            for entry in entries:
                e = entry[u'FL']
                sane_contact = dict(map(lambda x: (x['val'], x['content']), e))
                sane_contacts.append(sane_contact)
        else:
            e = entries[u'FL']
            sane_contact = dict(map(lambda x: (x['val'], x['content']), e))
            sane_contacts.append(sane_contact)
        return sane_contacts
    
    def update_database(self):
        try:
            latest_contact = Contact.objects.latest('modified_time')
            latest = latest_contact.modified_time.astimezone(pytz.utc).strftime('%Y-%m-%d%%20%H:%M:%S')
        except Contact.DoesNotExist:
            latest = "1970-01-01%2012:00:00"
        contacts = self.get_contacts(latest)
        for contact in contacts:
            try:
                c = Contact.objects.get(contact_id=contact[u'CONTACTID'])
            except Contact.DoesNotExist:
                c = Contact(contact_id=contact[u'CONTACTID'])
            c.first_name = contact[u'First Name']
            c.last_name = contact['Last Name']
            try:
                c.email = contact[u'Email']
            except KeyError:
                pprint(contact)
            try:
                c.membership_status = contact[u'Membership Status']
            except KeyError:
                pprint(contact)
            modified_time = datetime.strptime(contact[u'Modified Time'], '%Y-%m-%d %H:%M:%S')
            modified_time = modified_time.replace(tzinfo=pytz.utc)
            pprint(modified_time)
            c.modified_time = modified_time
            c.save()


if __name__ == '__main__':
    from pprint import pprint
    zc = ZohoClient()
    zc.update_database()

