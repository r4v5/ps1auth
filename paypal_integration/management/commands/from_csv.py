from django.core.management.base import BaseCommand, CommandError
from paypal_integration.models import Transaction
from datetime import datetime, timedelta
from pprint import pprint
import pytz
from moneyed import Money
from csv import DictReader
from dateutil.parser import parse
import codecs
import paypal_integration.models

class Command(BaseCommand):

    def handle(self, *args, **options):
        for file_name in args:
            csv_file = codecs.open(file_name, 'rb', 'cp1252')
            encoded_file = codecs.iterencode(csv_file, 'utf-8')
            self.consume_csv(encoded_file)

    def consume_csv(self, file_handle):
        data = DictReader(file_handle)
        for t in data:
            transaction = Transaction(id=t[' Transaction ID'])
            timestamp_string = "{} {} {}".format(t['Date'], t[' Time'], t[' Time Zone'])
            timestamp = parse(timestamp_string)
            #timestamp = datetime.strptime(timestamp_string, "%m/%d/%Y %H:%M:%S").replace(tzinfo=pytz.timezone(t[' Time Zone']))
            transaction.timestamp = timestamp
            transaction.type = t[' Type']
            transaction.from_email = t[' From Email Address']
            transaction.to_email = t[' To Email Address']
            transaction.name = t[' Name']
            transaction.status = t[' Status']
            if ' Gross' in t:
                transaction.amount = Money(t[' Gross'].replace(',',''), 'USD')
            if ' Fee' in t and t[' Fee'] != '...':
                transaction.fee_amount = Money(t[' Fee'], 'USD')
            if ' Net' in t:
                transaction.net_amount = Money(t[' Net'].replace(',',''), 'USD')

            if t[' Balance'] != '...':
                transaction.balance = Money(t[' Balance'].replace(',',''), 'USD')
            if ' Reference Txn ID' in t and t[' Reference Txn ID'] != '':
                try:
                    referenced_transaction = Transaction.objects.get(id=t[' Reference Txn ID'])
                    transaction.reference = referenced_transaction
                except Transaction.DoesNotExist:
                    print(("Skipping filling in reference for {}->{}".format(transaction.id, t[' Reference Txn ID'])))
            transaction.save()
