from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render
import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def hello_world(request):
    t = get_template("hello_world.html")
    context = RequestContext(request)
    html = t.render(context)
    return HttpResponse(html)

def login(request):
    if request.method == 'POST':
        form = AutenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Redirect to a success page.
                else:
                    pass
                    #reutnr a 'disabled account' error message
            else:
                pass
                #return an 'invalid login' error message
    
def logout(request):
    logout(request)
    
def activate_account(request):
    if request.method == 'POST':
        form = forms.activate_account_form(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(reverse('accounts.views.activation_email_sent'))
    else:
        form = forms.activate_account_form()
    return render(request, 'activate_account.html', {
        'form': form,
        })

def activation_email_sent(request):
    return render(request, 'activate_account_email_sent.html')

def account_activate_confirm(request, token):
    context = RequestContext(request)
    if request.method == 'POST':
        form = forms.account_register_form(request.POST)
        if form.is_valid():
            user = form.save()
    else:
        form = forms.account_register_form()
        context['form'] = form
        t = get_template('account_register.html')
    t = get_template('account_register.html')
    return HttpResponse(t.render(context))


