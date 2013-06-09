from django import forms
from zoho_integration.models import Contact, Token
import uuid
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
import accounts.backends
from django.conf import settings
import ldap

class activate_account_form(forms.Form):
    ps1_email = forms.EmailField(label="PS1 Email")

    def clean_ps1_email(self):
        try:
            contact = Contact.objects.get(email=self.cleaned_data['ps1_email'])
        except Contact.DoesNotExist:
            raise forms.ValidationError("Unknown Email Address")
        return self.cleaned_data['ps1_email']

    def save(self):
        email_address = self.cleaned_data['ps1_email']
        # HEFTODO check email against AD
        zoho_contact = Contact.objects.get(email=email_address)
        token = Token(token=uuid.uuid4(), zoho_contact=zoho_contact)
        token.save()
        c = {
                'email': email_address,
                'token': token.token,
                'protocol': 'http', # HEFTODO detemine if dev or not
                'domain': 'localhost:8000' # HEFTODO determine if dev or not
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
    password1 = forms.CharField(widget = forms.PasswordInput)
    password2 = forms.CharField(widget = forms.PasswordInput)

    def clean_preferred_username(self):
        username = self.cleaned_data['preferred_username']
        l = accounts.backends.get_ldap_connection()
        filter_string = '(sAMAccountName={0})'.format(username)
        result = l.search_s(settings.AD_BASEDN, ldap.SCOPE_SUBTREE, filterstr=filter_string)
        if result:
            error_string = "Account name {0} already in use.".format(username)
            raise forms.ValidationError(error_string)
        return username

    def save(self):
        user_dn = "CN={0},{1}".format(self.cleaned_data['preferred_username'], settings.AD_BASEDN)
        user_attrs = {}
        user_attrs['objectClass'] = ['top', 'person', 'organizationalPerson', 'user']
        user_attrs['cn'] = str(self.cleaned_data['preferred_username'])
        user_attrs['userPrincipalName'] = str(self.cleaned_data['preferred_username'] + '@' + settings.AD_DOMAIN)
        user_attrs['sAMAccountName'] = str(self.cleaned_data['preferred_username'])
        user_attrs['givenName'] = str(self.cleaned_data['first_name'])
        user_attrs['sn'] = str(self.cleaned_data['last_name'])
        user_attrs['userAccountControl'] = '514'
        user_ldif = modlist.addModlist(user_attrs)

        # Prep the password
        unicode_pass = '\"' + self.cleaned_data['password1'] + '\"'
        password_value = unicode_pass.encode('utf-16-le')
        add_pass = [(ldap.MOD_REPLACE, 'unicodePwd', [password_value])]

        # prep account enable
        mod_acct = [(ldap.MOD_REPLACE, 'userAccountControl', '512')]

        ldap_connection = accounts.backends.get_ldap_connection()

        # Add user
 #       try:
        ldap_connection.add_s(user_dn, user_ldif)
#        except ldap.LDAPError, error_message:
#            print(error_message)
#            return False

        # Add the password
#        try:
        ldap_connection.modify_s(user_dn, add_pass)
#        except ldap.LDAPError, error_messages:
#            print("bad things")
#            return False

#        try:
        ldap_connection.modify_s(user_dn, mod_acct)
#        except ldap.LDAPError, error_messages:
#            print("could not enable user")
#            return False

        ldap_connection.unbind_s()

        return True
