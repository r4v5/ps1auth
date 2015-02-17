import uuid
from django import forms
from django.template import loader
from member_management.models import Person, EmailRecord
from .models import Token


class activate_account_form(forms.Form):
    ps1_email = forms.EmailField(label="PS1 Email")

    def clean_ps1_email(self):
        try:
            contact = Person.objects.get(email=self.cleaned_data['ps1_email'])
        except Person.DoesNotExist:
            raise forms.ValidationError("Unknown Email Address")
        if contact.user is not None:
            #HEFTODO an account recovery link would be nice.
            raise forms.ValidationError("Your Account has already been activated")

        return self.cleaned_data['ps1_email']

    def save(self, use_https, domain):
        email_address = self.cleaned_data['ps1_email']
        # HEFTODO check email against AD
        person = Person.objects.get(email=email_address)
        token = Token(token=uuid.uuid4(), person=person)
        token.save()
        c = {
                'email': email_address,
                'token': token.token,
                'protocol': 'https' if use_https else 'http',
                'domain': domain,
        }
        subject = loader.render_to_string("signup/activation_email_subject.txt", c)
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string("signup/activation_email_body.txt", c)
        EmailRecord.objects.send_email(
            user=None,
            from_email='noreply@pumpingstationone.org',
            reply_to_email=None,
            to_person=person,
            subject=subject,
            text_content=body,
        )
