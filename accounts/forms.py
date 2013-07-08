from django.contrib.sites.models import get_current_site
from django.template import loader
from django import forms
from django.contrib.auth import get_user_model
from accounts.models import PS1User
from .tokens import default_token_generator

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
        email = self.cleaned_data["email"]
        users = PS1User.objects.get_users_by_field("mail", self.cleaned_data['email'])
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
            c = {
                'email': email,
                'domain': domain,
                'site_name': site_name,
                #'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # django's confirmation step calls urlsafe_base64_decode on the uid
                # actually, head uses that, 1.5 uses int_to_base36
                'uid': user.object_guid,
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            user_email = user.ldap_user['mail'][0]
            send_mail(subject, email, from_email, [user_email])


