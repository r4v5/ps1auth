from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from django.views.generic import RedirectView
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'auth.views.home', name='home'),
    url(r'^$', RedirectView.as_view(permanent=False, url='/zinc/member_list')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^rfid/', include('rfid.urls')),
    url(r'^zinc/', include('zoho_integration.urls')),
    url(r'^pod/', include('paypal_integration.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

