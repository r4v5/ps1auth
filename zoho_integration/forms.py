import ldap
import ldap.modlist
import uuid
from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from accounts.backends import PS1Backend, get_ldap_connection
from accounts.models import PS1User
from zoho_integration.models import Contact, Token

class activate_account_form(forms.Form):
    ps1_email = forms.EmailField(label="PS1 Email")

    def clean_ps1_email(self):
        try:
            contact = Contact.objects.get(email=self.cleaned_data['ps1_email'])
        except Contact.DoesNotExist:
            raise forms.ValidationError("Unknown Email Address")
        if contact.user is not None:
            #HEFTODO an account recovery link would be nice.
            raise forms.ValidationError("Your Account has already been activated")

        return self.cleaned_data['ps1_email']

    def save(self, use_https, domain):
        email_address = self.cleaned_data['ps1_email']
        # HEFTODO check email against AD
        zoho_contact = Contact.objects.get(email=email_address)
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
        send_mail(subject, body, "hef@pbrfrat.com", [email_address])

class account_register_form(forms.Form):
    preferred_username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    preferred_email = forms.EmailField()
    #password1 = forms.CharField(widget = forms.PasswordInput)
    #password2 = forms.CharField(widget = forms.PasswordInput)
    token = forms.CharField(widget = forms.HiddenInput())

    def clean_preferred_username(self):
        username = self.cleaned_data['preferred_username']
        l = get_ldap_connection()
        filter_string = '(sAMAccountName={0})'.format(username)
        result = l.search_s(settings.AD_BASEDN, ldap.SCOPE_SUBTREE, filterstr=filter_string)
        if result:
            error_string = "A member is already using '{0}' as his or her username.".format(username)
            raise forms.ValidationError(error_string)
        return username

    def save(self):
        """ Create the user
        A lot of this functionality needs to be moved to PS1UserManager, and
        some of the duplicate functionality needs with the accounts module
        needs to be refactored.
        """
        token = Token.objects.get(token=self.cleaned_data['token'])
        user_dn = "CN={0},{1}".format(self.cleaned_data['preferred_username'], settings.AD_BASEDN)
        user_attrs = {}
        user_attrs['objectClass'] = ['top', 'person', 'organizationalPerson', 'user']
        user_attrs['cn'] = str(self.cleaned_data['preferred_username'])
        user_attrs['userPrincipalName'] = str(self.cleaned_data['preferred_username'] + '@' + settings.AD_DOMAIN)
        user_attrs['sAMAccountName'] = str(self.cleaned_data['preferred_username'])
        user_attrs['givenName'] = str(self.cleaned_data['first_name'])
        user_attrs['sn'] = str(self.cleaned_data['last_name'])
        user_attrs['userAccountControl'] = '514'
        user_attrs['mail'] = str(self.cleaned_data['preferred_email']) 
        user_ldif = ldap.modlist.addModlist(user_attrs)

        # prep account enable
        enable_account = [(ldap.MOD_REPLACE, 'userAccountControl', '512')]

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
        token.zoho_contact.user = user
        token.zoho_contact.save()
        token.delete()

        #ldap_connection.modify_s(user_dn, add_pass)
        ldap_connection.modify_s(user_dn, enable_account)

        ldap_connection.unbind_s()

        return user
