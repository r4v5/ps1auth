# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class Contact(scrapy.Item):
    date_of_birth = Field()
    first_name = Field()
    full_name = Field()
    last_name = Field()
    mailing_street = Field()
    mailing_line_2 = Field()
    mailing_city = Field()
    mailing_country = Field()
    mailing_state = Field()
    mailing_zip = Field()
    membership_start_date = Field()
    membership_end_date = Field()
    membership_status = Field()
    payment_type = Field()
    salutation = Field()
    secondary_email = Field()
    primary_email = Field()
    contact_id = Field()
    payment_type = Field()

class EmailRecord(scrapy.Item):
    contact_zoho_crm_id = Field()
    msg_id = Field()
    from_email = Field()
    to_email = Field()
    subject = Field()
    sent_time = Field()
    body = Field()

class Note(scrapy.Item):
    note_id = Field()
    parent_contact_id = Field()
    title = Field()
    body = Field()
    created_at = Field()
    by = Field()
