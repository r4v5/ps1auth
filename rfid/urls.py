from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'configure/$', 'rfid.views.configure_rfid', {}),
    url(r'check/(?P<resource_name>\w+)/(?P<tag_number>[0-9a-fA-F]{12})$', 'rfid.views.check_ascii', {}),
    url(r'check/(?P<resource_name>\w+)/(?P<tag_number>[0-9a-fA-F]{6,7})$', 'rfid.views.check', {}),
)
