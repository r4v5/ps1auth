import ldap
import ldap.modlist
import re
import uuid
from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from accounts.backends import PS1Backend, get_ldap_connection
from accounts.models import PS1User
from zoho_integration.models import Token
from member_management.models import Person

class activate_account_form(forms.Form):
    ps1_email = forms.EmailField(label="PS1 Email")

    def clean_ps1_email(self):
        try:
            contact = person.objects.get(email=self.cleaned_data['ps1_email'])
        except person.DoesNotExist:
            raise forms.ValidationError("Unknown Email Address")
        if contact.user is not None:
            #HEFTODO an account recovery link would be nice.
            raise forms.ValidationError("Your Account has already been activated")

        return self.cleaned_data['ps1_email']

    def save(self, use_https, domain):
        email_address = self.cleaned_data['ps1_email']
        # HEFTODO check email against AD
        zoho_contact = person.objects.get(email=email_address)
        token = Token(token=uuid.uuid4(), zoho_contact=zoho_contact)
        token.save()
        c = {
                'email': email_address,
                'token': token.token,
                'protocol': 'https' if use_https else 'http',
                'domain': domain,
        }
        subject = render_to_string("activation_email_subject.txt", c)
        subject = ''.join(subject.splitlines())
        body = render_to_string("activation_email_body.html", c)
        send_mail(subject, body, "noreply@pumpingstationone.org", [email_address])

class account_register_form(forms.Form):
    preferred_username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    preferred_email = forms.EmailField()
    token = forms.CharField(widget = forms.HiddenInput())

    def clean_preferred_username(self):
        username = self.cleaned_data['preferred_username']
        l = get_ldap_connection()
        filter_string = '(sAMAccountName={0})'.format(username)
        result = l.search_s(settings.AD_BASEDN, ldap.SCOPE_SUBTREE, filterstr=filter_string)
        if result:
            error_string = "A member is already using '{0}' as his or her username.".format(username)
            raise forms.ValidationError(error_string)

        if not re.match(r"^[a-z][a-z0-9]{2,30}$", username):
            error_string = """Username must be all lower case,
            start with a letter,
            contain only letters and numbers,
            and be between 3 and 30 characters"""
            raise(forms.ValidationError(error_string))

        return username

    def save(self):
        """ Create the user
        A lot of this functionality needs to be moved to PS1UserManager, and
        some of the duplicate functionality needs with the accounts module
        needs to be refactored.
        """
        token = Token.objects.get(token=self.cleaned_data['token'])
                
        username = str(self.cleaned_data['preferred_username'])
        first_name = str(self.cleaned_data['first_name'])
        last_name = str(self.cleaned_data['last_name'])
        email = str(self.cleaned_data['preferred_email'])
        
        user = PS1User.objects.create_user(username, email=email, first_name=first_name, last_name=last_name)
        token.zoho_contact.user = user
        token.zoho_contact.save()
        token.delete()

        return user
