from django import forms
from django.core.mail import send_mail
import uuid
from django.template.loader import render_to_string
import ldap
import ldap.modlist as modlist
from django.conf import settings
from accounts import backends
from django.core.exceptions import ValidationError
from zoho_integration.models import Contact


