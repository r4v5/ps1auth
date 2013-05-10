from django import forms

class ActivateForm(forms.Form):
    ps1_email = forms.EmailField()
