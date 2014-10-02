from django import forms
from ckeditor.widgets import CKEditorWidget

class wysiwyg(forms.Form):
    from_email = forms.CharField(label='From')
    reply_to = forms.CharField()
    subject = forms.CharField()
    content = forms.CharField(widget=CKEditorWidget())



