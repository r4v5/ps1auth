from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

EMAIL_BACKEND = 'django.core.mail.backends.EmailBackend'
SERVER_EMAIL = 'no-reply@arbitrarion.com'

INSTALLED_APPS += (
)

INTERNAL_IPS = (
)

ALLOWED_HOSTS = [
    'arbitrarion.com',
    'www.arbitrarion.com',
]

MIDDLEWARE_CLASSES += (
)

STATIC_ROOT = "/srv/http/arbitrarion.com/static"
MEDIA_ROOT = "/srv/http/arbitrarion.com/media"
