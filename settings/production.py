from .base import *

DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SERVER_EMAIL = 'no-reply@members.pumpingstationone.org'

ADMINS = (
    ('Hef', 'hef+ps1auth@pbrfrat.com'),
)

INSTALLED_APPS += (
)

INTERNAL_IPS = (
)

ALLOWED_HOSTS = [
    'members.pumpingstationone.org',
    'www.members.pumpingstationone.org',
]

MIDDLEWARE_CLASSES += (
)

STATIC_ROOT = "/srv/http/members.pumpingstationone.org/static"
MEDIA_ROOT = "/srv/http/members.pumpingstationone.org/media"
