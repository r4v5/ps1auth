from django.db import models
from django.conf import settings
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist
from django.core.mail import EmailMultiAlternatives
from datetime import date
from email.mime.image import MIMEImage
import os
from smtplib import SMTPException


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
    class Meta:
        abstract = True

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

class EmailRecordManager(models.Manager):
    
    def send_recorded_email(self, user, from_email, to_person, subject, body_template_prefix, attachments = [], inline_image_files = []):
        text_content = render_to_string("{}.txt".format(body_template_prefix), {})
        email_message = EmailMultiAlternatives(subject, text_content, from_email, [to_person.email])
        try:
            html_content = render_to_string("{}.html".format(body_template_prefix), {})
            email_message.attach_alternative(html_content, "text/html")
            email_message.mixed_subtype = 'related'
        except TemplateDoesNotExist:
            pass

        # inline images
        for image_file in inline_image_files: 
            file = open(image_file, 'rb')
            image = MIMEImage(file.read())
            file.close()
            image.add_header('Content-ID', "<{}>".format(os.path.basename(image_file)))

        # regular attachments
        for attachment in attachments:
            email_message.attach_file(attachment)

        # Record the email
        email_record = EmailRecord(
            subject=subject,
            message = email_message.message(),
            from_email = from_email,
            to_email = to_person.email,
            recipient = to_person,
            sender = user,
        )
        email_record.save()

        # Send
        try:
            email_message.send(fail_silently=False)
            email_record.status = 'sent'
            email_record.save()
            return 1
        except SMTPException:
            email_record.statis = 'failed'
            email_record.save()
            return 0

class EmailRecord(models.Model):
    subject = models.CharField(max_length=128)
    message = models.TextField()
    from_email = models.EmailField()
    reply_to_email = models.EmailField(null=True, blank=True)
    to_email = models.EmailField()
    sender = models.ForeignKey(settings.AUTH_USER_MODEL)
    recipient = models.ForeignKey('CRMPerson')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = EmailRecordManager()
    status = models.CharField(default='pending', max_length=30)

    class Meta:
        ordering = ['-created_at']

