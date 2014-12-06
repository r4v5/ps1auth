# Create your views here
import re

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext

import forms
from models import Token

def activate_account(request):
    if request.method == 'POST':
        form = forms.activate_account_form(request.POST)
        if form.is_valid():
            site = get_current_site(request)
            user = form.save( request.is_secure(), site.domain)
            return HttpResponseRedirect(reverse('signup.views.activation_email_sent'))
    else:
        form = forms.activate_account_form()
    return render(request, 'activate_account.html', {
        'form': form,
        })

def activation_email_sent(request):
    return render(request, 'activate_account_email_sent.html')

def account_activate_confirm(request, token):
    try:
        token = Token.objects.get(token=token)
    except Token.DoesNotExist:
        messages.error(request, "Unknown Account Activation URL")
        return HttpResponseRedirect(reverse('signup.views.activate_account'))
    zoho_contact = token.zoho_contact 
    if request.method == 'POST':
        form = forms.account_register_form(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'accounts.backends.PS1Backend'
            login(request, user)
            return HttpResponseRedirect(reverse('accounts.views.set_password'))
    else:
        data = {}
        data['first_name'] = zoho_contact.first_name
        data['last_name'] = zoho_contact.last_name
        data['preferred_email'] = zoho_contact.email
        data['token'] = token.token
        form = forms.account_register_form(initial=data)
    return render(request, 'account_register.html', {
        'form': form,
    })
