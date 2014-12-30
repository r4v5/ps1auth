from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from .filters import PersonFilter
from .forms import PersonForm, IDCheckForm, PayPalForm, PersonSearchForm
from .models import Person, EmailTemplate, EmailRecord, IDCheck
from .tables import PersonTable
from math import ceil
import reversion
from django_tables2 import RequestConfig

@staff_member_required
def send_templated_email(request, email_template_id, person_id=None):
    email_template = EmailTemplate.objects.get(pk = email_template_id)
    if person_id:
        recipient = Person.objects.get(pk=person_id)
    else:
        recipient = None
    count = email_template.send(request.user, recipient)
    if count == 1:
        messages.success(request, 'Sent "{}" to "{}'.format(email_template, recipient))
    elif count == 0:
        messages.error(request, 'Failed to Send "{}" to "{}'.format(email_template, recipient))
    else:
        messages.info(request, "sending {} to {} recipients".format(email_template, count))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

@staff_member_required
def send_test_templated_email(request, email_template_id):
    return send_templated_email(request, email_template_id, person_id=request.user.person.pk)

@login_required()
def member_list(request):
    data = {}
    data['full_members'] = Person.objects.full_members().order_by('last_name')
    data['starving_hackers'] = Person.objects.starving_hackers().order_by('last_name')
    data['member_count'] = Person.objects.members().count()
    data['quorum_count'] = max(int(ceil(float(data['full_members'].count() / 3))), 1)
    return render(request, 'member_management/member_list.html', data)

@staff_member_required
def person_detail(request, person_id):
    try:
        person = Person.objects.get(pk=person_id)
    except Person.DoesNotExist:
        person = None
    if person and hasattr(person, 'paypal'):
        paypal = person.paypal
    else:
        paypal = None

    if request.method == 'POST':
        person_form = PersonForm(request.POST, prefix='person', instance=person)
        paypal_form = PayPalForm(request.POST, prefix='paypal', instance=paypal)
        # avoid short circuit evaluation
        person_form_is_valid = person_form.is_valid()
        paypal_form_is_valid = person_form.is_valid()
        if person_form_is_valid and paypal_form_is_valid:
            with transaction.atomic(), reversion.create_revision():
                person = person_form.save()
                paypal = paypal_form.save(commit=False)
                paypal.person = person
                paypal.save()
                reversion.set_user(request.user)
                messages.success(request, 'Saved Changes Successfully')
                return HttpResponseRedirect(person.get_absolute_url())
    else:
        person_form = PersonForm(prefix='person', instance=person)
        paypal_form = PayPalForm(prefix='paypal', instance=paypal)
    data = {}
    data['person_form'] = person_form
    data['paypal_form'] = paypal_form
    data['email_records'] = EmailRecord.objects.filter(recipient=person)
    data['person'] = person
    data['id_checks'] = IDCheck.objects.filter(person=person)
    return render(request, 'member_management/detail.html', data)

def person_list(request): 
    # poor mans search
    search_form = PersonSearchForm(request.GET)

    if search_form.is_valid():
        queryset = search_form.get_queryset()
    else:
        queryset = Person.objects.all()
    data = {}
    table = PersonTable(queryset)
    RequestConfig(request, paginate={'per_page':100}).configure(table)
    data['table'] = table
    data['search_form'] = search_form
    return render(request, 'member_management/person_list.html', data)
