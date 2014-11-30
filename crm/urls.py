from django.conf.urls import patterns, url

urlpatterns = patterns('crm.views',
    url(r'send_templated_email/(?P<email_template_id>\d+)/(?P<person_id>\d+)$', 'send_templated_email', {}),
    url(r'send_templated_email/(?P<email_template_id>\d+)$', 'send_templated_email', {}),
)
