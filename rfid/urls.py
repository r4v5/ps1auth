from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'configure/$', 'rfid.views.configure_rfid', {}),
    url(r'check/(?P<resource_name>\w+)/(?P<tag_number>\w+)$', 'rfid.views.check', {}),
)
