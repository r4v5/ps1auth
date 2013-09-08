from .base import *

DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SERVER_EMAIL = 'systems@members.pumpingstationone.org'

ADMINS = (
    ('Hef', 'hef+ps1auth@pbrfrat.com'),
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(SITE_ROOT, '..', 'cache'),
    }
}

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
