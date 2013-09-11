from .base import *

DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SERVER_EMAIL = 'no-reply@arbitrarion.com'

ADMINS = (
    ('Hef', 'hef+arbitrairon@pbrfrat.com'),
)
MERCHANT_SETTINGS = {
    'pay_pal': {
        #'RECEIVER_EMAIL': 'hef+paypalsandbox@pbrfrat.com',
        'RECEIVER_EMAIL': 'money@pumpingstationone.org',
    }
}
PAYPAL_RECEIVER_EMAIL = MERCHANT_SETTINGS['pay_pal']['RECEIVER_EMAIL']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(SITE_ROOT, '..', 'cache')
    }
}

INSTALLED_APPS += (
)

INTERNAL_IPS = (
)

ALLOWED_HOSTS = [
    'arbitrarion.com',
    'www.arbitrarion.com',
]

SESSION_COOKIE_SECURE = True

MIDDLEWARE_CLASSES += (
)

STATIC_ROOT = "/srv/http/arbitrarion.com/static"
MEDIA_ROOT = "/srv/http/arbitrarion.com/media"
