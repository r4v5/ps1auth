from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from .models import MemberPoint
from .forms import GrantMemberPointForm
import reversion



@login_required
def list(request):
    context = {}
    context['points'] = MemberPoint.objects.valid()
    context['consumed_points'] = MemberPoint.objects.consumed
    return render(request, 'memberpoint/list.html', context)

class MemberPointFormView(FormView):
    template_name = 'memberpoint/form.html'
    form_class = None
    title = None
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(MemberPointFormView, self).get_context_data(**kwargs)
        context['debug'] = kwargs
        context['title'] = self.title
        context['points'] = kwargs['owner'].memberpoint_set.valid()
        return context

    def form_valid(self, form):
        return super(MemberPointFormView, self).form_valid(form)

    def get(self, request, user_id):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.fields['owner'].initial = user_id
        owner = get_user_model().objects.get(pk=user_id)
        context = self.get_context_data(form=form, owner=owner)
        return self.render_to_response(context)

    def post(self, request, user_id):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            with transaction.atomic(), reversion.create_revision():
                form.save()
                messages.success(request, 'Memberpoint action completed')
                reversion.set_user(request.user)
            return HttpResponseRedirect(request.get_full_path())
        else:
            return self.form_invalid(form)

    @method_decorator(staff_member_required)
    def dispath(self, *args, **kwargs):
        return super(MemberPointFormView, self).dispath(*args, **kwargs)
