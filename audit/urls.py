from django.conf.urls import patterns, include, url
import accounts.views

urlpatterns = patterns('',
    url(r'foobar/$', 'audit.views.foobar', {}),
    url(r'audits/$', 'audit.views.audits', {}),
)
