from django.db import models
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.template import Context, Template
from datetime import date
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
import os
from smtplib import SMTPException
from ckeditor.fields import RichTextField
import re
from html2text import html2text
from bs4 import BeautifulSoup


# Create your models here.
class CRMPersonManager(models.Manager):

    def full_members(self):
        return super(CRMPersonManager, self).get_queryset().filter(membership_status='full_member')

    def members(self):
        return super(CRMPersonManager, self).get_queryset().filter(Q(membership_status='full_member')|Q(membership_status='starving_hacker'))

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
    membership_status = models.CharField(max_length=128, choices=MEMBERSHIP_LEVEL, default='discontinued')
    membership_start_date = models.DateField(default=date.today)
    street_address = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=128)
    id_check_1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='id_checker_1', null=True, blank=True)
    id_check_2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='id_checker_2', null=True, blank=True)
    objects = CRMPersonManager()

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

    def send_email(self, user, from_email, to_person, subject, html_content = None, text_content = None, attachments = []):
        """
        @param attachements a list of MIMEBase objects
        """
        total_emails_sent  = 0
        total_emails_failed = 0
        email_message = EmailMultiAlternatives(subject, text_content, from_email, [to_person.email])
        if html_content:
            email_message.attach_alternative(html_content, "text/html")
            email_message.mixed_subtype = 'related'

            # attachements
            for attachment in attachments: 
                email_message.attach(attachment)

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
                total_emails_sent += 1
            except SMTPException:
                email_record.statis = 'failed'
                email_record.save()
                total_emails_failed += 1
        return total_emails_sent

class EmailRecord(models.Model):
    subject = models.CharField(max_length=128)
    message = models.TextField()
    from_email = models.EmailField()
    reply_to_email = models.EmailField(blank=True)
    to_email = models.EmailField()
    sender = models.ForeignKey(settings.AUTH_USER_MODEL)
    recipient = models.ForeignKey('CRMPerson')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = EmailRecordManager()
    status = models.CharField(default='pending', max_length=30)

    class Meta:
        ordering = ['-created_at']

class EmailTemplateManager(models.Manager):

    def individual_recipient(self):
        return self.filter(recipients='individual')

class EmailTemplate(models.Model):
    RECIPIENTS = (
            ('all_members', 'All Members'),
            ('full_members', 'Full Members'),
            ('individual', 'Individual'),
    )
    from_email = models.EmailField(verbose_name = 'From')
    reply_to_email = models.EmailField(verbose_name = 'Reply-To', blank=True)
    recipients = models.CharField(max_length=128, choices=RECIPIENTS, default='full_members')
    subject = models.CharField(max_length=128)
    message = RichTextField()
    objects = EmailTemplateManager()

    def __unicode__(self):
        return u'{}'.format(self.subject)

    def _convert_inline_images(self, html_content):
        soup = BeautifulSoup(html_content)
        attachments = []
        for tag in soup.find_all("img", src=re.compile("^{}".format(settings.MEDIA_URL))):
            basename = os.path.basename(tag['src'])
            #slice media_url off
            m = re.match("^{}(.*)".format(settings.MEDIA_URL), tag['src'])
            relative_file = m.group(1)
            #append file path to MEDIA_ROOT
            absolute_file = os.path.join(settings.MEDIA_ROOT, relative_file)
            image_file = open(absolute_file, 'rb')
            image = MIMEImage(image_file.read())
            image_file.close()
            image.add_header('Content-ID', "<{}>".format(basename))
            attachments.append(image)
            # rewrite tag in src
            tag['src'] = "cid:{}".format(basename)
        return (str(soup), attachments)

    def _send(self, user, target, extra_context):
        extra_context['recipient'] = target
        t = Template(self.message)
        message = t.render(Context(extra_context))
        html_content, attachments = self._convert_inline_images(message)
        txt_content = html2text(html_content)
        for attachment in self.attachments.all():
            file_data = MIMEApplication(attachment.file.read())
            attachments.append(file_data)
        return EmailRecord.objects.send_email(user, self.from_email, target, self.subject, html_content, txt_content, attachments);

    def send(self, user, target = None, extra_context = {}):
        total = 0
        if target:
            total += self._send(user, target, extra_context)
        elif self.recipients == 'all_members':
            for member in CRMPerson.objects.members():
                total += self._send(user, member, extra_context)
        elif self.recipients == 'full_members':
            for member in CRMPerson.objects.full_members():
                total += self._send(user, member, extra_context)
        return total

class EmailAttachement(models.Model):
    email = models.ForeignKey('EmailTemplate', related_name='attachments')
    file = models.FileField(upload_to="email_attachements")

