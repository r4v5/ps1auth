from django.db import models
from django.conf import settings
from datetime import date


# Create your models here.
class CRMPerson(models.Model):
    MEMBERSHIP_LEVEL = (
            ('discontinued', 'Discontinued'),
            ('starving_hacker', 'Starving Hacker'),
            ('full_member', 'Full Member'),
            ('suspended', 'Suspended'),
            ('banned', 'Banned'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField()
    birthday = models.DateField()
    membership_status = models.CharField(max_length=128, choices=MEMBERSHIP_LEVEL, default='Discontinued')
    membership_start_date = models.DateField(default=date.today)
    street_address = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=128)
    id_check_1 = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='id_checker_1', null=True)
    id_check_2 = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='id_checker_2', null=True)

    def __unicode__(self):
        return u'{0} {1}'.format(self.first_name, self.last_name)

class CRMPaymentMethod(models.Model):
    person = models.OneToOneField('CRMPerson', null=True)
    pass

class PayPal(CRMPaymentMethod):
    email = models.EmailField()
    paid_up_until = models.DateField(blank=True, null=True)
    class Meta:
        verbose_name = 'PayPal'
        verbose_name_plural = 'PayPal'

class Cash(CRMPaymentMethod):
    paid_up_until = models.DateField(blank=True)
    class Meta:
        verbose_name = 'cash'
        verbose_name_plural = 'cash'

class Note(models.Model):
    person = models.ForeignKey('CRMPerson')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

class EmailTemplate(models.Model):
    subject = models.CharField(max_length=256)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
