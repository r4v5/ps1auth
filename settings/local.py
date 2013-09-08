from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(SITE_ROOT, 'cache'),
    }
}

INSTALLED_APPS += (
    "debug_toolbar",
)

INTERNAL_IPS = (
    "127.0.0.1",
)

MIDDLEWARE_CLASSES += (
    "debug_toolbar.middleware.DebugToolbarMiddleware",
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}


