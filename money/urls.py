from django.conf.urls import patterns, include, url
from billing import get_integration
pay_pal = get_integration("pay_pal")


urlpatterns = patterns('money.views',
    url(r'^create/$', 'create_customer', {}),
    url(r'^add_credit_card/$', 'add_credit_card', {}),
    url(r'^subscribe/$', 'subscribe', {}),
)
