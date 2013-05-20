from django import forms
from django.confcore.mail import send_mail


class account_activate_form(forms.Form):
    ps1_email = forms.EmailField()

    def save(self):
        email_address = self.ps1_email.cleaned_data['ps1_email']
        # HEFTODO check email against zoho
        # HEFTODO check email against AD
        c = {
                'email': user.email,
                'token': str(uuid.uuid4()),
        }
        subject = load.render_to_string("activation_email_subject.txt", c)
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string("activation_email_body.html", c)
        send_mail(subject, email, from_email, [email_address])



