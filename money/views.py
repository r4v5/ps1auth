# Create your views here.
from django.dispatch import reciever
from billing.signals import transaction_was_successful


@reciever(transaction_was_successful)
def handle_successful_transaction(sender, type, response):
    raise Exception

@reiver(transaction_was_unsuccessful)
def handle_unsuccessful_transaction(sender, type, response):
    raise Exception
