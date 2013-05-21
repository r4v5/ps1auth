from django import forms
from django.core.mail import send_mail
import uuid
from django.template.loader import render_to_string


class activate_account_form(forms.Form):
    ps1_email = forms.EmailField()

    def save(self):
        email_address = self.cleaned_data['ps1_email']
        # HEFTODO check email against zoho
        # HEFTODO check email against AD
        c = {
                'email': email_address,
                'token': str(uuid.uuid4()),
        }
        subject = render_to_string("activation_email_subject.txt", c)
        subject = ''.join(subject.splitlines())
        body = render_to_string("activation_email_body.html", c)
        send_mail(subject, email, from_email, [email_address])



