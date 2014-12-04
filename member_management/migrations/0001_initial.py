# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table(u'member_management_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['accounts.PS1User'], unique=True, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('membership_status', self.gf('django.db.models.fields.CharField')(default='discontinued', max_length=128)),
            ('membership_start_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('street_address', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal(u'member_management', ['Person'])

        # Adding model 'IDCheck'
        db.create_table(u'member_management_idcheck', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['member_management.Person'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.PS1User'])),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'member_management', ['IDCheck'])

        # Adding model 'PayPal'
        db.create_table(u'member_management_paypal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['member_management.Person'], unique=True, null=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('paid_up_until', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'member_management', ['PayPal'])

        # Adding model 'Cash'
        db.create_table(u'member_management_cash', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['member_management.Person'], unique=True, null=True)),
            ('paid_up_until', self.gf('django.db.models.fields.DateField')(blank=True)),
        ))
        db.send_create_signal(u'member_management', ['Cash'])

        # Adding model 'Note'
        db.create_table(u'member_management_note', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['member_management.Person'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'member_management', ['Note'])

        # Adding model 'EmailRecord'
        db.create_table(u'member_management_emailrecord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('from_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('reply_to_email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('to_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.PS1User'])),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['member_management.Person'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='pending', max_length=30)),
        ))
        db.send_create_signal(u'member_management', ['EmailRecord'])

        # Adding model 'EmailTemplate'
        db.create_table(u'member_management_emailtemplate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('from_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('reply_to_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('reply_to_email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('recipients', self.gf('django.db.models.fields.CharField')(default='full_members', max_length=128)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('message', self.gf('ckeditor.fields.RichTextField')()),
        ))
        db.send_create_signal(u'member_management', ['EmailTemplate'])

        # Adding model 'EmailAttachement'
        db.create_table(u'member_management_emailattachement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.related.ForeignKey')(related_name='attachments', to=orm['member_management.EmailTemplate'])),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'member_management', ['EmailAttachement'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table(u'member_management_person')

        # Deleting model 'IDCheck'
        db.delete_table(u'member_management_idcheck')

        # Deleting model 'PayPal'
        db.delete_table(u'member_management_paypal')

        # Deleting model 'Cash'
        db.delete_table(u'member_management_cash')

        # Deleting model 'Note'
        db.delete_table(u'member_management_note')

        # Deleting model 'EmailRecord'
        db.delete_table(u'member_management_emailrecord')

        # Deleting model 'EmailTemplate'
        db.delete_table(u'member_management_emailtemplate')

        # Deleting model 'EmailAttachement'
        db.delete_table(u'member_management_emailattachement')


    models = {
        u'accounts.ps1user': {
            'Meta': {'object_name': 'PS1User'},
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'object_guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '48', 'primary_key': 'True', 'db_index': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'member_management.cash': {
            'Meta': {'object_name': 'Cash'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid_up_until': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['member_management.Person']", 'unique': 'True', 'null': 'True'})
        },
        u'member_management.emailattachement': {
            'Meta': {'object_name': 'EmailAttachement'},
            'email': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attachments'", 'to': u"orm['member_management.EmailTemplate']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'member_management.emailrecord': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'EmailRecord'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['member_management.Person']"}),
            'reply_to_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.PS1User']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '30'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'to_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        },
        u'member_management.emailtemplate': {
            'Meta': {'object_name': 'EmailTemplate'},
            'from_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'from_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('ckeditor.fields.RichTextField', [], {}),
            'recipients': ('django.db.models.fields.CharField', [], {'default': "'full_members'", 'max_length': '128'}),
            'reply_to_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'reply_to_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'member_management.idcheck': {
            'Meta': {'object_name': 'IDCheck'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['member_management.Person']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.PS1User']"})
        },
        u'member_management.note': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Note'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['member_management.Person']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'member_management.paypal': {
            'Meta': {'object_name': 'PayPal'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid_up_until': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['member_management.Person']", 'unique': 'True', 'null': 'True'})
        },
        u'member_management.person': {
            'Meta': {'object_name': 'Person'},
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'membership_start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'membership_status': ('django.db.models.fields.CharField', [], {'default': "'discontinued'", 'max_length': '128'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['accounts.PS1User']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['member_management']