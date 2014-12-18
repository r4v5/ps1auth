from django.conf.urls import patterns, url

urlpatterns = patterns('member_management.views',
    url(r'send_templated_email/(?P<email_template_id>\d+)/(?P<person_id>\d+)$', 'send_templated_email', {}),
    url(r'send_templated_email/(?P<email_template_id>\d+)$', 'send_templated_email', {}),
    url(r'member_list', 'member_list', {}),
)
