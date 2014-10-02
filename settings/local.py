from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

MERCHANT_SETTINGS = {
    'pay_pal': {
        'RECEIVER_EMAIL': 'money@pumpingstationone.org',
    }
}
PAYPAL_RECEIVER_EMAIL = MERCHANT_SETTINGS['pay_pal']['RECEIVER_EMAIL']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(SITE_ROOT, 'cache'),
    }
}

INSTALLED_APPS += (
#    "debug_toolbar",
    "django_jenkins",
)

INTERNAL_IPS = (
    "127.0.0.1",
)

MIDDLEWARE_CLASSES += (
#    "debug_toolbar.middleware.DebugToolbarMiddleware",
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}


