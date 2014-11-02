from django.core.management.base import BaseCommand
from pprint import pprint
import json
from crm.models import CRMPerson, Note, EmailRecord, PayPal, Cash
import dateutil.parser
from django.conf import settings
from accounts.models import PS1User
from pytz import timezone


tz = timezone('America/Chicago')
membership_status_map = {
    'Full Membership': 'full_member',
    'PS1 Starving Hacker Membership': 'starving_hacker',
    'discontinued': 'discontinued',
    'not a member': 'discontinued',
    'banned': 'banned',
    'Pumping Station: One - Pay What You Want': 'full_member',
    'Friend of PS:One': 'not a member',
    'suspended': 'suspended',
    'PS1 Full Membership': 'full_member',
}

class Command(BaseCommand):


    def handle(self, *args, **options):
        data = json.loads(open(args[0],'rb').read())
        id_map = {}

        for person in CRMPerson.objects.all():
            person.delete()

        for entry in data:
            if entry.has_key('contact_id'):
                crm_person = CRMPerson()
                id_map[entry['contact_id']] = crm_person
                dob = entry['date_of_birth']
                if dob:
                    crm_person.birthday = dateutil.parser.parse(dob)
                crm_person.city = entry['mailing_city']
                crm_person.first_name = entry['first_name']

                # for some reason the last name field contains the first name and salutation
                if entry['salutation']:
                    starter_text = entry['salutation'] + " " + entry['first_name']
                else:
                    starter_text = entry['first_name']
                if entry['last_name'].strip().startswith(starter_text):
                    crm_person.last_name = entry['last_name'].strip()[len(starter_text):].strip()
                else:
                    crm_person.last_name = entry['last_name'].strip()
                
                crm_person.email = entry['primary_email'] 
                crm_person.street_address = entry['mailing_street'] 
                crm_person.mailing_city = entry['mailing_city'] 
                crm_person.mailing_state = entry['mailing_state'] 
                crm_person.zip_code = entry['mailing_zip'] 
                crm_person.country = entry['mailing_country'] 

                start_date = entry['membership_start_date']
                if start_date:
                    crm_person.membership_start_date = dateutil.parser.parse(start_date)

                crm_person.membership_status = membership_status_map[entry['membership_status']]
                crm_person.save()


                if entry['payment_type'] == 'Paypal' and (entry['primary_email'] or entry['secondary_email']):
                    paypal = PayPal()
                    paypal.person = crm_person
                    if  entry['secondary_email']:
                        paypal.email = entry['secondary_email']
                    else:
                        paypal.email = entry['primary_email']
                    if entry['membership_end_date']:
                        paypal.paid_up_until = dateutl.parser.parse(entry['membership_end_date']).replace(tzinfo=tz)
                    paypal.save()

                elif entry['payment_type'] == 'Cash' and entry['membership_end_date']:
                    cash = Cash()
                    cash.person = crm_person
                    cash.paid_up_until = dateutl.parser.parse(entry['membership_end_date']).replace(tzinfo=tz)
                    cash.save()
                



        for entry in data:
            if entry.has_key('note_id'):
                note = Note()
                note.person = id_map[entry['parent_contact_id']]
                if entry['title']:
                    note.content = entry['title'].strip() + ": " + entry['body']
                else:
                    note.content = entry['body']
                note.save()
                note.created_at = dateutil.parser.parse(entry['created_at']).replace(tzinfo=tz)
                note.save()

            elif entry.has_key('msg_id'):
                email_record = EmailRecord()
                email_record.sender = PS1User.objects.first()
                email_record.recipient = id_map[entry['contact_zoho_crm_id']]
                email_record.subject = entry['subject']
                email_record.to_email = entry['to_email']
                email_record.from_email = entry['from_email']
                email_record.message = entry['body']
                email_record.status = "zoho"
                email_record.save()
                email_record.created_at = dateutil.parser.parse(entry['sent_time']).replace(tzinfo=tz)
                email_record.save()

        def id_check():
            pass
