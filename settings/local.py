from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS += (
    "debug_toolbar",
)

INTERNAL_IPS = (
    "127.0.0.1",
)

MIDDLEWARE_CLASSES += (
    "debug_toolbar.middleware.DebugToolbarMiddleware",
)

AD_BINDDN = get_env_variable("AD_BINDDN")
AD_BINDDN_PASSWORD = get_env_variable("AD_BINDDN_PASSWORD")

