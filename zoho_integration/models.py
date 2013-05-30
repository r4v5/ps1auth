from django.db import models

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
# Create your models here.
