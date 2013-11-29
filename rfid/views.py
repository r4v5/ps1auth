from .models import Resource, RFIDNumber
from .forms import KeyForm
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import RequestContext


def check(request, resource_name, tag_number):
    try:
        tag = RFIDNumber.objects.get(number=tag_number)
        resource = Resource.objects.get(name=resource_name)
    except (RFIDNumber.DoesNotExist, Resource.DoesNotExist):
        return HttpResponse(content="No", status=404, reason="Resource or Tag not Found")
    if resource.is_allowed(tag):
        return HttpResponse(content="Yes", status=200, reason="Access Allowed")
    else:
        return HttpResposne(content="No", status=403, reason="Access Denied")


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

