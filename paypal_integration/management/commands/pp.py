from django.core.management.base import BaseCommand, CommandError
from paypal_integration.models import Transaction
from paypal import PayPalConfig, PayPalInterface
from datetime import datetime, timedelta
from pprint import pprint
import pytz
from moneyed import Money

CONFIG = PayPalConfig(
    API_USERNAME="",
    API_PASSWORD="",
    API_SIGNATURE="",
    API_ENVIRONMENT="PRODUCTION",
    DEBUG_LEVEL=0,
)

class Command(BaseCommand):

    def handle(self, *args, **options):
        now = datetime.now() - timedelta(days=30)

        try:
            latest = Transaction.objects.latest('timestamp').timestamp
        except Transaction.DoesNotExist:
            latest = datetime.now() - timedelta(days=365*5)

        pprint(latest)
        paypal = PayPalInterface(CONFIG)
        result = paypal.transaction_search(startdate=latest)
        print "grabbed %d items" % len(result.items())
        for item in result.items():
            error = False
            transaction = Transaction(id=item['TRANSACTIONID'])
            transaction.timestamp = datetime.strptime(item[u'TIMESTAMP'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.UTC)
            transaction.type = item[u'TYPE']
            try:
                transaction.email = item[u'EMAIL']
            except KeyError:
                error = True
            transaction.name = item[u'NAME']
            transaction.status = item[u'STATUS']
            try:
                transaction.amount = Money(item[u'AMT'], item[u'CURRENCYCODE'])
            except KeyError:
                error = True
            try:
                transaction.fee_amount = Money(item[u'FEEAMT'], item[u'CURRENCYCODE'])
            except KeyError:
                error = True
            try:
                transaction.net_amount = Money(item[u'NETAMT'], item[u'CURRENCYCODE'])
            except KeyError:
                error = True

            if error:
                pprint(item)
            transaction.save()

