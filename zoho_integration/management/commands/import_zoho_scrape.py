from django.core.management.base import BaseCommand
from pprint import pprint
import json
from crm.models import CRMPerson, Note, EmailRecord, PayPal, Cash, IDCheck
import dateutil.parser
from django.conf import settings
from accounts.models import PS1User
from pytz import timezone
import re


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

zoho_user_to_ps1user_map = {
    'hef': 'hef',
    'Bry': 'bry',
    'Derek': 'dbever',
    'bry': 'bry',
    'Steve': 'stevetheotherone',
    'Farkas': 'stevetheotherone',
    'Everett': 'negativek',
    'Anthony': 'anthony',
    'derek': 'dbever',
    'DB': 'dbever',
    'steve': 'stevetheotherone',
    'everett': 'negativek',
    'Jay': 'neilsboring',
    'Hef': 'hef',
    'Noonie': 'noony', #todo create an account for noony
    'Loans': 'dbever',
}

id_check_regex_list = [
    r'^ID Check(( -)|(:)) (?P<checker>\w+)(\n)+I[dD] [Cc]heck(( -)|(:)) (?P<checker2>\w+)$',
    r'^(ID )?[cC]heck(ed)? by (?P<checker>\w+) and (?P<checker2>\w+)((\.)|(\s+)|(\n))?$',
    r'^Verified by (?P<checker>\w+) And (?P<checker2>\w+)$',
    r'^I[Dd] [Cc]hecked( by)? (?P<checker>\w+) and (?P<checker2>\w+) \d{1,4}[-/]\d{2}[-/]\d{2,4}$',
    r'^ID checked by (?P<checker>\w+) 8-19-2014 and (?P<checker2>\w+).',
    r'^(?P<checker>\w+) and (?P<checker2>\w+) checked ID$',
    r'id check, (?P<checker>\w+) (?P<checker2>\w+)',
    r'Verified by (?P<checker>\w+) and (?P<checker2>\w+)',
    r'^(ID|Id|id) [cC]heck(ed)?( (by|-)|:)? (?P<checker>\w+)(( - .+)|(, .+)|(\.))?$',
    r'^Verified By (?P<checker>\w+) (?P<checker2>\w+)$',


    r'^Verified by (?P<checker>\w+) ,still needs door code and welcome email.$',
    r'^ID Check (?P<checker>\w+) \d{1,2}/\d{2}/\d{4}(\n)?$',
    r'^(?P<checker>\w+) Entered and view \d{1,2}/\d{2}/\d{4}$',
    r'^(?P<checker>\w+) checked ID.$',
    r'^ID says: Charles Dennis Runcie\nID Check: (?P<checker>\w+)$',
    r'^ID checked --(?P<checker>\w+) \(and (?P<checker2>\w+)\)$',
    r'^id checked -- (?P<checker>\w+)$',
    r'^id check -(?P<checker>\w+)$',
    r'^Checked by (?P<checker>\w+)(( as well\.)|(\.))?$',
    r'^Checked by (?P<checker>\w+)(( as well\.)|(\.))?$',
    r'^Second check done by (?P<checker>\w+)\.$',
    r'ID check : (?P<checker>\w+) \(needs a second id check\)',
    r'^ID was checked by (?P<checker>\w+). Needs another board member.$',
    r'^Checked ID - (?P<checker>\w+)$',
]

not_an_id_regex_list = [
    r'^Heavy Quip Inc\.$',
    r'^\$140 for payment through October received\.$',
    r'PayPal',
    r'Paypal',
    r'paypal',
    r'((.* )|(^))[Pp]oints?(( .*)|($))',
    r'^.{140,}$',
    r'^\$\d+ (check )?((received)|(dated)) 2014[-/]\d{2}[-/]\d{2}\.?$',
    r'member point',
    r'[\w\.]+@\w+\.\w+',
    r'^\$.*',
    r'.* \$40\ .*',
    r'^Also goes by:.*$',
    r'membership',
    r'paid',

]

class Command(BaseCommand):


    def handle(self, *args, **options):
        data = json.loads(open(args[0],'rb').read())
        self.id_map = {}

        for person in CRMPerson.objects.all():
            person.delete()

        for entry in data:
            if entry.has_key('contact_id'):
                crm_person = CRMPerson()
                self.id_map[entry['contact_id']] = crm_person
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

                if (entry['payment_type'] == 'Paypal' and entry['primary_email']) or entry['secondary_email']:
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

            if self.id_check(entry):
                pass
            elif entry.has_key('note_id'):
                note = Note()
                note.person = self.id_map[entry['parent_contact_id']]
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
                email_record.recipient = self.id_map[entry['contact_zoho_crm_id']]
                email_record.subject = entry['subject']
                email_record.to_email = entry['to_email']
                email_record.from_email = entry['from_email']
                email_record.message = entry['body']
                email_record.status = "zoho"
                email_record.save()
                email_record.created_at = dateutil.parser.parse(entry['sent_time']).replace(tzinfo=tz)
                email_record.save()

    def id_check(self, entry):
        if entry.has_key('note_id'):
            for regex in id_check_regex_list:
                #try:
                    m = re.match(regex,entry['body'])
                    if m:
                        checker = m.groupdict()['checker']
                        if checker in ['Needs']:
                            continue
                        #print(checker, regex, entry['body'])
                        #pprint(m.groupdict())
                        username = zoho_user_to_ps1user_map[checker]
                        user = PS1User.objects.get_users_by_field("sAMAccountName", username)[0]
                        id_check = IDCheck(
                            user = user,
                            note = entry['body'],
                            person = self.id_map[entry['parent_contact_id']]
                        )
                        id_check.save()
                        id_check.created_at = dateutil.parser.parse(entry['created_at']).replace(tzinfo=tz)
                        id_check.save()


                        if m.groupdict().has_key('checker2'):
                            username = zoho_user_to_ps1user_map[checker]
                            user = PS1User.objects.get_users_by_field("sAMAccountName", username)[0]
                            id_check = IDCheck(
                                user = user,
                                note = entry['body'],
                                person = self.id_map[entry['parent_contact_id']]
                            )
                            id_check.save()
                            id_check.created_at = dateutil.parser.parse(entry['created_at']).replace(tzinfo=tz)
                            id_check.save()


                        return True
                #except Exception as e:
                #    pprint("Failed")
                #    pprint(entry)
                #    raise e
            for regex in not_an_id_regex_list:
                #pprint((regex,entry))
                m = re.match(regex,entry['body'])
                if m:
                    return False
            pprint(entry['body'][:240])
        return False
