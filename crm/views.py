from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import CRMPerson, EmailTemplate

@staff_member_required
def send_templated_email(request, email_template_id, person_id):
    email_template = EmailTemplate.objects.get(pk = email_template_id)
    recipient = CRMPerson.objects.get(pk=person_id)
    count = email_template.send(request.user, recipient)
    if count == 1:
        messages.success(request, 'Sent "{}" to "{}'.format(email_template, recipient))
    elif count == 0:
        messages.error(request, 'Failed to Send "{}" to "{}'.format(email_template, recipient))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

