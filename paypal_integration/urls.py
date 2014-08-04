from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'reports/$', 'paypal_integration.views.reports', {}),
    url(r'report/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', 'paypal_integration.views.report', {}),
)
