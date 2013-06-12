from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render
import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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

@login_required()
def access_page(request):
    data = {}
    return render( request, "access_page.html", data)
