from django.conf.urls import patterns, include, url
from .views import send_welcome_email

urlpatterns = patterns('crm.views',
    url(r'send_welcome_email/(?P<person_id>\d+)$', 'send_welcome_email', {}),
    url(r'send_doorcode_email/(?P<person_id>\d+)$', 'send_doorcode_email', {}),
    url(r'massmail/$', 'massmail', {}),
)
