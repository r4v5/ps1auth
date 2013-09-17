from .models import Resource, RFIDNumber
from .forms import KeyForm
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import RequestContext


def validate(request, resource, tag_number):
    tag = RFIDNumber.objects.get(number=tag)
    resource = Resource.objects.get(name)
    if resource.is_allowed(tag):
        return HttpResponse(status_code=200)
    else:
        return HttpResposne(status_code=403)


@login_required()
def configure_rfid(request):
    try:
        tag = request.user.rfidnumber
    except RFIDNumber.DoesNotExist:
        tag = RFIDNumber(user=request.user)
    if request.method == 'POST':
        form = KeyForm(request.POST, instance=tag)
        if form.is_valid():
            foo = form.save(commit=False)
            foo.save()
            messages.success(request, "RFID tag number updated")
    else:
        request.user.rfidnumber
        form = KeyForm(instance=tag)
    t = get_template("configure_rfid.html")
    context = RequestContext(request)
    context["form"] = form
    html = t.render(context)
    return HttpResponse(html)

