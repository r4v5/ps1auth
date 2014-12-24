from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'activate/$', 'zoho_integration.views.activate_account', {}),
    url(r'activate/email_sent$', 'zoho_integration.views.activation_email_sent', {}),
    url(r'activate/confirm/(?P<token>.*)$', 'zoho_integration.views.account_activate_confirm', {}),
    #url(r'member_list$', 'zoho_integration.views.member_list', {}),
)
