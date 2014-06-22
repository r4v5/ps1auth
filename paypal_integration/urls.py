from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'report/$', 'paypal_integration.views.report', {}),
    url(r'statements/$', 'paypal_integration.views.statements', {}),
    url(r'statement/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', 'paypal_integration.views.statement', {}),
)
