from django.db import models
import accounts.models

class Contact(models.Model):
    MEMBERSHIP_STATUS_CHOICES = (
            ('Full', 'Full Membership'),
            ('Starving', 'Starving Hacker'),
    )
    contact_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=300)
    membership_status = models.CharField(max_length=300, choices=MEMBERSHIP_STATUS_CHOICES)
    modified_time = models.DateTimeField()
    user = models.OneToOneField(accounts.models.PS1User, null=True)

class Token(models.Model):
    token = models.CharField(max_length=36)
    zoho_contact = models.ForeignKey(Contact)
