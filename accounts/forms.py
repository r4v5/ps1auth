from django.contrib.sites.models import get_current_site
from django.template import loader
from django import forms
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models import PS1User
#from .tokens import default_token_generator
from .models import PendingMember, EmergencyContact
from .tokens import *
from .backends import PS1Backend, get_ldap_connection
import ldap
from bootstrap_toolkit.widgets import BootstrapDateInput
from  localflavor.us.forms import USZipCodeField
import ldap.modlist
import re

class PasswordResetForm(forms.Form):
    """ 
    Form grabbed from https://github.com/django/django/blob/6118d6d1c982e428cf398ac998eb9f0baba15bad/django/contrib/auth/forms.py#L210-L250
    """
    email = forms.EmailField(label=("Email"), max_length=254)

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        from django.core.mail import send_mail
        UserModel = get_user_model()
        email_address = self.cleaned_data["email"]
        users = PS1User.objects.get_users_by_field("mail", email_address)
        for user in users:
            # Make sure that no email is sent to a user that actually has
            # a password marked as unusable

            #HEFTODO implement has_unusable_password
            #if not user.has_usable_password():
            #    continue
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            # ignore the token_generator that was passed in
            token = default_token_generator.make_token(user)
            c = {
                'email': email_address,
                'domain': domain,
                'site_name': site_name,
                'uid': user.object_guid,
                'user': user,
                'token': token,
                'protocol': 'https' if use_https else 'http',
            }
            if not from_email:
                from_email = settings.SERVER_EMAIL
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email_body = loader.render_to_string(email_template_name, c)
            user_email = user.ldap_user['mail'][0]
            send_mail(subject, email_body, from_email, [user_email])

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set his/her password without entering the
    old password
    ripped from https://github.com/django/django/blob/6118d6d1c982e428cf398ac998eb9f0baba15bad/django/contrib/auth/forms.py#L253-L285
    """
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    new_password1 = forms.CharField(label="New password",
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="New password confirmation",
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def clean(self):
        """
        Warning, this function does the actualy password resetting.
        """
        try:
            password = self.cleaned_data.get('new_password1') or ""
            self.user.set_password(password)
        except ldap.CONSTRAINT_VIOLATION as e:
            raise forms.ValidationError(e[0]['info'])
        return self.cleaned_data

    def save(self, commit=True):
        """
        Warning, this function Does no do work, the actual work is doen in clean()
        """
        return self.user


class PersonalInfoForm(forms.ModelForm):
    zip_code = USZipCodeField(initial=606)
    class Meta:
        model = PendingMember
        widgets = {
            'date_of_birth': BootstrapDateInput(),
        }

class EmergencyContactForm(forms.ModelForm):
    class Meta:
        exclude = ['member']
        model = EmergencyContact


class verifyID(forms.Form):
    member = forms.CharField()
    name = forms.BooleanField()
    address = forms.BooleanField()
    date_of_birth = forms.BooleanField()

    def __init__():
        pass

class account_register_form(forms.Form):
    preferred_username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    preferred_email = forms.EmailField()

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
        user_dn = "CN={0},{1}".format(self.cleaned_data['preferred_username'], settings.AD_BASEDN)
        user_attrs = {}
        user_attrs['objectClass'] = ['top', 'person', 'organizationalPerson', 'user']
        user_attrs['cn'] = str(self.cleaned_data['preferred_username'])
        user_attrs['userPrincipalName'] = str(self.cleaned_data['preferred_username'] + '@' + settings.AD_DOMAIN)
        user_attrs['sAMAccountName'] = str(self.cleaned_data['preferred_username'])
        user_attrs['givenName'] = str(self.cleaned_data['first_name'])
        user_attrs['sn'] = str(self.cleaned_data['last_name'])
        # Create the account "Disabled"
        user_attrs['userAccountControl'] = '514'
        user_attrs['mail'] = str(self.cleaned_data['preferred_email']) 
        user_ldif = ldap.modlist.addModlist(user_attrs)

        ldap_connection = get_ldap_connection()

        # add the user to AD
        result = ldap_connection.add_s(user_dn, user_ldif)

        #now get the user guid
        filter_string = r'sAMAccountName={0}'.format(str(self.cleaned_data['preferred_username']))
        result = ldap_connection.search_ext_s(settings.AD_BASEDN, ldap.SCOPE_ONELEVEL, filterstr=filter_string)
        ldap_user = result[0][1]
        guid = uuid.UUID(bytes_le=ldap_user['objectGUID'][0])
        user = PS1Backend().get_user(guid)
        user.save()

        ldap_connection.unbind_s()

        return user
