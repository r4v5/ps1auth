# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'EmailAttachement'
        db.delete_table(u'crm_emailattachement')

        # Deleting model 'Cash'
        db.delete_table(u'crm_cash')

        # Deleting model 'CRMPerson'
        db.delete_table(u'crm_crmperson')

        # Deleting model 'Note'
        db.delete_table(u'crm_note')

        # Deleting model 'EmailRecord'
        db.delete_table(u'crm_emailrecord')

        # Deleting model 'IDCheck'
        db.delete_table(u'crm_idcheck')

        # Deleting model 'PayPal'
        db.delete_table(u'crm_paypal')

        # Deleting model 'EmailTemplate'
        db.delete_table(u'crm_emailtemplate')


    def backwards(self, orm):
        # Adding model 'EmailAttachement'
        db.create_table(u'crm_emailattachement', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.related.ForeignKey')(related_name='attachments', to=orm['crm.EmailTemplate'])),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'crm', ['EmailAttachement'])

        # Adding model 'Cash'
        db.create_table(u'crm_cash', (
            ('person', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.CRMPerson'], unique=True, null=True)),
            ('paid_up_until', self.gf('django.db.models.fields.DateField')(blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'crm', ['Cash'])

        # Adding model 'CRMPerson'
        db.create_table(u'crm_crmperson', (
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('membership_status', self.gf('django.db.models.fields.CharField')(default='discontinued', max_length=128)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['accounts.PS1User'], unique=True, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('membership_start_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('street_address', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal(u'crm', ['CRMPerson'])

        # Adding model 'Note'
        db.create_table(u'crm_note', (
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.CRMPerson'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'crm', ['Note'])

        # Adding model 'EmailRecord'
        db.create_table(u'crm_emailrecord', (
            ('status', self.gf('django.db.models.fields.CharField')(default='pending', max_length=30)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('reply_to_email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.CRMPerson'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('to_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.PS1User'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('from_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'crm', ['EmailRecord'])

        # Adding model 'IDCheck'
        db.create_table(u'crm_idcheck', (
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.CRMPerson'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.PS1User'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'crm', ['IDCheck'])

        # Adding model 'PayPal'
        db.create_table(u'crm_paypal', (
            ('person', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.CRMPerson'], unique=True, null=True)),
            ('paid_up_until', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'crm', ['PayPal'])

        # Adding model 'EmailTemplate'
        db.create_table(u'crm_emailtemplate', (
            ('recipients', self.gf('django.db.models.fields.CharField')(default='full_members', max_length=128)),
            ('reply_to_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('from_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('reply_to_email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('message', self.gf('ckeditor.fields.RichTextField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('from_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'crm', ['EmailTemplate'])


    models = {
        
    }

    complete_apps = ['crm']