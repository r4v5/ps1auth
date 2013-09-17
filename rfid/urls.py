from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'configure/$', 'rfid.views.configure_rfid', {}),
)
