# Create your views here.
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django_braintree.forms import TransactionForm, CustomerForm, CreditCardForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import braintree

@login_required()
def create_customer(request):
    result = CustomerForm.get_result(request)
    pprint(result)
    if result and result.is_success:
        return HttpResponseRedirect("/")

    customer_form = CustomerForm(result, redirect_url='http://127.0.0.1:8000/money/create')
    customer_form.remove_section("customer")
    customer_form.tr_protected["customer"]["id"] = str(request.user.object_guid)
    customer_form.tr_fields["customer"]["first_name"] = str(request.user.first_name)
    customer_form.tr_fields["customer"]["last_name"] = str(request.user.last_name)
    customer_form.tr_fields["customer"]["email"] = str(request.user.email)
    customer_form.generate_tr_data()
    return render(request, "create_customer.html", {
        "form": customer_form,
    })

@login_required()
def add_credit_card(request):
    result = CreditCardForm.get_result(request)
    pprint(result)
    if result and result.is_success:
        return HttpResponseRedirect("/")

    credit_card_form = CreditCardForm(result, redirect_url='http://127.0.0.1:8000/money/add_credit_card')

    credit_card_form.tr_protected["credit_card"]["customer_id"] = str(request.user.object_guid)
    credit_card_form.tr_protected["credit_card"]["options"]['verify_card'] = True

    
    credit_card_form.generate_tr_data()
    return render(request, "add_credit_card.html", {
        "form": credit_card_form
    })

@login_required()
def subscribe(request):
    customer = braintree.Customer.find(str(request.user.object_guid))
    # catch exception, use S2S to create customer
    return render(request, "subscribe.html", {
        "form": None,
        "debug": customer.credit_cards,
        "cards": customer.credit_cards

    })



