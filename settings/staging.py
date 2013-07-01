from .base import *

DEBUG = False
TEMPLATE_DEBUG = Debug

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


