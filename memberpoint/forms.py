from django import forms
from django.contrib.auth import get_user_model
from django.forms import Form, ModelForm
from .models import MemberPoint


class GrantMemberPointForm(ModelForm):
    """ Adds a memberpoint
    requires form.owner be set before calling save()
    """

    success_message = "Memberpoint granted."

    def clean(self):
        super(GrantMemberPointForm, self).clean()
        if not self.owner:
            raise forms.ValidationError('No Owner assigned for new member point.')
        return self.cleaned_data

    def save(self, commit=True):
        memberpoint = super(GrantMemberPointForm, self).save(commit=False)
        memberpoint.owner = self.owner
        if commit:
            memberpoint.save()
        return memberpoint

    class Meta:
        model = MemberPoint
        fields = ['reason',]

class ConsumeMemberPointForm(Form):
    """ Consumes a member point
    requires that form.owner be set before saving.
    """

    success_message = "Memberpoint consumed."

    def save(self):
        point = self.owner.memberpoint_set.next_to_expire()
        point.consume()
        return point

    def clean(self):
        cleaned_data = super(ConsumeMemberPointForm, self).clean()
        if not self.owner.memberpoint_set.next_to_expire():
            raise forms.ValidationError(
                '%(username)s has no member points',
                params={
                    'username': self.owner.get_short_name()
                })

