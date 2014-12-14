from django import forms
from ckeditor.widgets import CKEditorWidget

class mailform(forms.Form):
    CHOICES = [('all_members','All Members'),('full_members','Full Members')]
    from_email = forms.EmailField(label='From')
    reply_to = forms.EmailField()
    recipients =  forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    subject = forms.CharField()
    content = forms.CharField(widget=CKEditorWidget())



