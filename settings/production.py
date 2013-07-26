from .base import *

DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SERVER_EMAIL = 'no-reply@vm.pumpingstationone.org'

ADMINS = (
    ('Hef', 'hef+ps1auth@pbrfrat.com'),
)

INSTALLED_APPS += (
)

INTERNAL_IPS = (
)

ALLOWED_HOSTS = [
    'vm.pumpingstationone.org',
    'www.vm.pumpingstationone.org',
]

MIDDLEWARE_CLASSES += (
)

STATIC_ROOT = "/srv/http/vm.pumpingstationone.org/static"
MEDIA_ROOT = "/srv/http/vm.pumpingstationone.org/media"
