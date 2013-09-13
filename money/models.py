from django.db import models
from django.dispatch import receiver
from billing.signals import transaction_was_successful, transaction_was_unsuccessful

@receiver(transaction_was_successful)
def handle_successful_transaction(sender, type, response, **kwargs):
    raise Exception

@receiver(transaction_was_unsuccessful)
def handle_unsuccessful_transaction(sender, type, response, **kwargs):
    raise Exception

#transaction_was_successful.connect(handle_successful_transaction)
#transaction_was_unsuccessful.connect(handle_unsuccessful_transaction)

# Create your models here.
