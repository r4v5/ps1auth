import os
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
from django.core.mail import send_mail
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import EmailRecord, CRMPerson
from .forms import mailform
from html2text import html2text
from django.template import Context, Template


@staff_member_required
def send_welcome_email(request, person_id):
    from_email = 'president@pumpingstationone.org'
    to_person = CRMPerson.objects.get(id=person_id)
    subject = 'Welcome to PS:One!'
    body_template_prefix = 'crm/new_member_email'

    # Attach new member packet
    attachements = [os.path.join(os.path.dirname(__file__), "templates", "crm", "welcome.pdf")]

    # Attach Bry's picture.
    inline_images = [os.path.join(os.path.dirname(__file__), "templates", "crm", "bry.jpeg")]
    result = EmailRecord.objects.send_recorded_email(request.user, from_email, to_person, subject, body_template_prefix, attachements, inline_images)
    if result == 0:
        message.error(request, 'Welcome Email Failed to Send')
    elif result == 1:
        messages.success(request, 'Welcome Email Sent.')

    # TODO make previous path explicit.
    # not all browsers set HTTP_REFERER
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

@staff_member_required
def send_doorcode_email(request, person_id):
    from_email = 'cto@pumpingstationone.org'
    to_person = CRMPerson.objects.get(id=person_id)
    subject = 'PS:One Door code'
    body_template_prefix = 'crm/door_code_email'
    result = EmailRecord.objects.send_recorded_email(request.user, from_email, to_person, subject, body_template_prefix)
    if result == 0:
        message.error(request, 'Door Code Email Failed to Send')
    elif result == 1:
        messages.success(request, 'Door Code Email Sent.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


def massmail(request):
    if request.method == 'POST':
        form = mailform(request.POST)
        if form.is_valid():
            for person in CRMPerson.objects.all():
                template = Template(form.cleaned_data['content'])
                context = Context({'recipient':person})
                rendered_html = template.render(context)
                rendered_txt = html2text(rendered_html)
                result = EmailRecord.objects.send_email(request.user, form.cleaned_data['from_email'], [person], form.cleaned_data['subject'], rendered_html, rendered_txt)
                if result == 0:
                    message.error(request, 'Failed to send email to {}.'.format(person.email))
                elif result == 1:
                    messages.success(request, 'Email sent to {}.'.format(person.email))
                else:
                    messages.info(request, 'sent some emails')
    else:
        form = mailform()
    context = {}
    context['form'] = form
    return render(request, 'crm/form.html', context)

