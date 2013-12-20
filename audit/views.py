from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import render

import ldap
import uuid

from accounts.backends import PS1Backend, get_ldap_connection
from accounts.models import PS1User
from zoho_integration.models import Contact

def foobar(request):
    data = {}
    return render(request, "foobar.html", data)

@user_passes_test(lambda u:u.is_staff )
def audits(request):
    l = get_ldap_connection()
    filter_string ='(ObjectClass=Person)'
    #sAMAccountName userAccountControl pwdLastSet
    users_result = l.search_ext_s(settings.AD_BASEDN ,ldap.SCOPE_ONELEVEL, filterstr=filter_string)
    users = []
    for user_result in users_result:
        guid = str( uuid.UUID( bytes_le=( user_result[1]['objectGUID'][0] ) ) )
        try:
            account = PS1User.objects.get(object_guid=guid)
            try:
                contact = account.contact
            except Contact.DoesNotExist:
                contact = None
        except PS1User.DoesNotExist:
            account = None
            contact = None

        end_date = None
        if contact:
            end_date = contact.membership_end_date

        user = {
            'name':       user_result[1]['sAMAccountName'][0],
            'enabled':    (int(user_result[1]['userAccountControl'][0]) & 2) != 2,
            'pwdLastSet': win32_filetime(user_result[1]['pwdLastSet'][0]),
            'contact':  contact,
            'account': account,
            'guid': str(guid),
            'end_date': end_date,
        }
        users.append(user)

    data = {}
    data["debug"] = paypal_payers()
    data["users"] = users
    data['payers'] = paypal_payers()
    return render( request, "audits.html", data )


from datetime import datetime, timedelta

def win32_filetime(filetime_timestamp):
    microseconds = int(filetime_timestamp) / 10.
    return datetime(1601,1,1) + timedelta(microseconds=microseconds)

from paypal.standard.ipn.models import PayPalIPN
def paypal_payers():
    return PayPalIPN.objects.order_by('payer_email', '-created_at').distinct('payer_email')

