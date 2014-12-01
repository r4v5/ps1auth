from django.db import models
import accounts.models
from datetime import datetime
import pytz

class Token(models.Model):
    token = models.CharField(max_length=36)
    zoho_contact = models.ForeignKey(Contact)

