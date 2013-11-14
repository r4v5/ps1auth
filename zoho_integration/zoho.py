#!/usr/bin/env python
from django.conf import settings
import urllib2
import json
from django.core.cache import cache
from zoho_integration.models import Contact, ContactChange
from datetime import datetime
import pytz

class ZohoClient(object):
    """ work in progress, Builds up a list of zoho users """
    api_key = settings.ZOHO_AUTHTOKEN

    def get_contacts(self, most_recent='1970-01-01%2012:00:00'):
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

            #attach the modified time  
            modified_time = datetime.strptime(contact[u'Modified Time'], '%Y-%m-%d %H:%M:%S')
            modified_time = modified_time.replace(tzinfo=pytz.utc)
            #pprint(modified_time)
            c.modified_time = modified_time
            c.save()

            ContactChange.log(c, 'first_name', contact[u'First Name'])
            ContactChange.log(c, 'last_name', contact[u'Last Name'])
            try:
                ContactChange.log(c, 'email', contact[u'Email'])
            except KeyError:
                print("Email not set for {}".format(contact))
            try:
                ContactChange.log(c, 'membership_status', contact[u'Membership Status'])
            except KeyError:
                print("No membership status for {}".format(contact))

            # Not all records will have this "Membership End Date"
            try:
                ends_on = datetime.strptime(contact[u'Membership End Date'], '%Y-%m-%d')
                ContactChange.log(c, 'membership_end_date', ends_on)
            except KeyError:
                pass
            c.save()

    def get_record(self, contact_id):
        url= ("https://crm.zoho.com/crm/private/json/Contacts/getRecordById?"
        "authtoken={0}&scope=crmapi&id={1}".format(self.api_key, contact_id))

        result = urllib2.urlopen(url)
        raw_output = result.read()                                                                                     
        response = json.loads(raw_output)
        return response

if __name__ == '__main__':
    from pprint import pprint
    import sys
    if len(sys.argv) > 1:
        zc = ZohoClient()
        record = zc.get_record(sys.argv[1])
        pprint(record)
