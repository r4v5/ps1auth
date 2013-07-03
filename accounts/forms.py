from django import forms

from accounts.models import PS1User


class PasswordResetForm(forms.Form):
    email = forms.EmailField()

    def save(self):
        users = PS1User.objects.get_users_by_field("mail", cleaned_data['email'])
        user = users[0]

