from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset_complete
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.template.loader import get_template
from django.template.response import TemplateResponse

from .tokens import default_token_generator
from .forms import SetPasswordForm
from .backends import PS1Backend
from .models import Token

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
                    #Redirect to a success page.
                else:
                    pass
                    #return a 'disabled account' error message
            else:
                pass
                #return an 'invalid login' error message

def logout(request):
    logout(request)

@login_required()
def access_page(request):
    data = {}
    return render( request, "access_page.html", data )

@login_required()
def set_password(request):
    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accounts.views.access_page'))
    else:
        form = SetPasswordForm(request.user)
    context = {
            'user': request.user,
            'form': form,
    }
    return render(
            request,
            'registration/password_reset_confirm.html',
            context)

def password_reset_confirm(request, uid=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    ripped from https://github.com/django/django/blob/d51b7794bfd1ddfd92f71f71d07daf931421c5f7/django/contrib/auth/views.py#L185-L229
    """
    UserModel = get_user_model()
    assert uid is not None and token is not None # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('django.contrib.auth.views.password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        uid = uid
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                token_object = Token.objects.get(key=token)
                token_object.delete()
                # HEFTODO I really could just log the user in here.
                # HEFTODO It would be smart to delete all the users tokens.
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(None)
    else:
        validlink = False
        form = None
    context = {
        'user': PS1Backend().get_user(uid),
        'form': form,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)
