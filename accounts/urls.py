from django.conf.urls import patterns, include, url
import accounts.views

urlpatterns = patterns('',
    url(r'profile/$', 'accounts.views.hello_world', name="profile"),
    url(r'login/$', 'django.contrib.auth.views.login', {}),
    url(r'logout/$', 'django.contrib.auth.views.logout', {}),
    url(r'password_change/$', 'django.contrib.auth.views.password_change', {}),
    url(r'password_change_done/$', 'django.contrib.auth.views.password_change_done', {}),
    url(r'password_reset/$', 'django.contrib.auth.views.password_reset', {}),
    url(r'password_reset_done/$', 'django.contrib.auth.views.password_reset_done', {}),
    url(r'password_reset_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)$', 'django.contrib.auth.views.password_reset_confirm', {}),
    url(r'password_reset_complete/$', 'django.contrib.auth.views.password_reset_complete', {}),
    url(r'activate/$', 'accounts.views.activate_account', {}),
    url(r'activate/confirm/(?P<token>.*)$', 'accounts.views.account_activate_confirm', {}),
)
