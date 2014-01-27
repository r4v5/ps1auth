from django import forms
import braintree
from django_braintree.forms import BraintreeForm
from django_braintree.odict import OrderedDict

class SignupForm(BraintreeForm):
    tr_type = "Customer"
    tr_fields = OrderedDict([
        ("customer", OrderedDict([
            ("first_name", None),
            ("last_name", None),
            ("company", None),
            ("email", None),
            ("phone", None),
            ("fax", None),
            ("website", None),
            ("credit_card", OrderedDict([
                ("cardholder_name", None),
                ("number", None),
                ("expiration_month", None),
                ("expiration_year", None),
                ("cvv", None),
                ("billing_address", OrderedDict([
                    ("first_name", None),
                    ("last_name", None),
                    ("company", None),
                    ("street_address", None),
                    ("extended_address", None),
                    ("locality", None),
                    ("region", None),
                    ("postal_code", None),
                    ("country_name", None)]),
                )]),
            )]),
        ),
    ])
    tr_labels = {
        "customer": {
            "credit_card": {
                "cvv": "CVV",
            },
        },
    }
    tr_protected = {
        "customer": {
            "id": None,
            "credit_card": {
                "token": None,
                "options": {
                    "verify_card": None,
                },
            },
        },
    }

    def __init__(self, *args, **kwargs):
        cardholder_name = kwargs.pop("cardholder_name", None)
        tr.tr_fields["customer"]["credit_card"]["cardholder_name"] = cardholder_name
        super(SignupForm, self).__init__(self, *args, **kwargs) 
