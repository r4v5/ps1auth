from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['127.0.0.1:8001', '127.0.0.1']


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
    "debug_toolbar",
#    "django_jenkins",
)

INTERNAL_IPS = (
    "127.0.0.1",
    "10.0.2.2",
)

MIDDLEWARE_CLASSES = (
    "debug_toolbar.middleware.DebugToolbarMiddleware",
) + MIDDLEWARE_CLASSES

MEDIA_ROOT = os.path.join(SITE_ROOT,'media')
MEDIA_URL = '/media/'

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

def show_toolbar(request):
    if not request.is_ajax() and str(request.user) == "hef":
        return True
    return False

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'settings.local.show_toolbar',
}

