from django import forms
from django.db.models import Q
from ckeditor.widgets import CKEditorWidget
from bootstrap3_datetime.widgets import DateTimePicker
from .models import Person, PayPal

class mailform(forms.Form):
    CHOICES = [('all_members','All Members'),('full_members','Full Members')]
    from_email = forms.EmailField(label='From')
    reply_to = forms.EmailField()
    recipients =  forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    subject = forms.CharField()
    content = forms.CharField(widget=CKEditorWidget())

class PersonForm(forms.ModelForm):
    class Meta:
        fields = ['user', 'first_name', 'last_name', 'email', 'birthday',
                'membership_status', 'membership_start_date', 'street_address',
                'unit_number', 'city', 'state', 'zip_code', 'country']
        widgets = {
                'user': forms.TextInput(attrs={'readonly':'readonly'}),
                'membership_start_date': DateTimePicker(options={"format": "YYYY-MM-DD","pickTime":False}),
                'birthday': DateTimePicker(options={"format": "YYYY-MM-DD","pickTime":False}),
        }
        model = Person

class IDCheckForm(forms.Form):
    government_issued = forms.BooleanField()

class PayPalForm(forms.ModelForm):

    #same_as_personal_email = forms.BooleanField(required=False)
    email = forms.EmailField(required=False, label="PayPal Email")
    class Meta:
        fields = ['email']
        model = PayPal

class PersonSearchForm(forms.Form):
    """ My Poor mans's search function """
    membership_status = forms.ChoiceField(choices=(('','--'),) + Person.MEMBERSHIP_LEVEL, required=False)
    search = forms.CharField(label='Search', required=False)
    
    def get_queryset(self):
        search = self.cleaned_data['search']
        membership_status = self.cleaned_data['membership_status']
        if membership_status:
            queryset = Person.objects.filter(membership_status=membership_status)
        else:
            queryset = Person.objects.all()
        return queryset.filter(
            Q(first_name__icontains=search)|
            Q(last_name__icontains=search)|
            Q(email__icontains=search)|
            Q(paypal__email__icontains=search)
        )
