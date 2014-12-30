from django import forms
from django.contrib.auth import get_user_model
from django.forms import Form, ModelForm
from .models import MemberPoint


class GrantMemberPointForm(ModelForm):
    class Meta:
        model = MemberPoint
        fields = ['reason', 'owner']
        widgets = {'owner': forms.HiddenInput()}

class ConsumeMemberPointForm(Form):
    owner = forms.CharField(widget=forms.HiddenInput())

    def save(self):
        user_id = self.cleaned_data['owner']
        user = get_user_model().objects.get(pk=user_id)
        point = user.memberpoint_set.next_to_expire()
        point.consume()
        return point




