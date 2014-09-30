# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CRMPerson'
        db.create_table(u'crm_crmperson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['accounts.PS1User'], unique=True, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('birthday', self.gf('django.db.models.fields.DateField')()),
            ('membership_status', self.gf('django.db.models.fields.CharField')(default='Discontinued', max_length=128)),
            ('membership_start_date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('street_address', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('id_check_1', self.gf('django.db.models.fields.related.OneToOneField')(related_name='id_checker_1', unique=True, null=True, to=orm['accounts.PS1User'])),
            ('id_check_2', self.gf('django.db.models.fields.related.OneToOneField')(related_name='id_checker_2', unique=True, null=True, to=orm['accounts.PS1User'])),
        ))
        db.send_create_signal(u'crm', ['CRMPerson'])

        # Adding model 'PayPal'
        db.create_table(u'crm_paypal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.CRMPerson'], unique=True, null=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('paid_up_until', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'crm', ['PayPal'])

        # Adding model 'Cash'
        db.create_table(u'crm_cash', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['crm.CRMPerson'], unique=True, null=True)),
            ('paid_up_until', self.gf('django.db.models.fields.DateField')(blank=True)),
        ))
        db.send_create_signal(u'crm', ['Cash'])

        # Adding model 'Note'
        db.create_table(u'crm_note', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.CRMPerson'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'crm', ['Note'])

        # Adding model 'EmailRecord'
        db.create_table(u'crm_emailrecord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('from_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('reply_to_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('to_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.PS1User'])),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.CRMPerson'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='pending', max_length=30)),
        ))
        db.send_create_signal(u'crm', ['EmailRecord'])


    def backwards(self, orm):
        # Deleting model 'CRMPerson'
        db.delete_table(u'crm_crmperson')

        # Deleting model 'PayPal'
        db.delete_table(u'crm_paypal')

        # Deleting model 'Cash'
        db.delete_table(u'crm_cash')

        # Deleting model 'Note'
        db.delete_table(u'crm_note')

        # Deleting model 'EmailRecord'
        db.delete_table(u'crm_emailrecord')


    models = {
        u'accounts.ps1user': {
            'Meta': {'object_name': 'PS1User'},
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'object_guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '48', 'primary_key': 'True', 'db_index': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'crm.cash': {
            'Meta': {'object_name': 'Cash'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid_up_until': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['crm.CRMPerson']", 'unique': 'True', 'null': 'True'})
        },
        u'crm.crmperson': {
            'Meta': {'object_name': 'CRMPerson'},
            'birthday': ('django.db.models.fields.DateField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_check_1': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'id_checker_1'", 'unique': 'True', 'null': 'True', 'to': u"orm['accounts.PS1User']"}),
            'id_check_2': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'id_checker_2'", 'unique': 'True', 'null': 'True', 'to': u"orm['accounts.PS1User']"}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'membership_start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'membership_status': ('django.db.models.fields.CharField', [], {'default': "'Discontinued'", 'max_length': '128'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['accounts.PS1User']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'crm.emailrecord': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'EmailRecord'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crm.CRMPerson']"}),
            'reply_to_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.PS1User']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '30'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'to_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        },
        u'crm.note': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Note'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crm.CRMPerson']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'crm.paypal': {
            'Meta': {'object_name': 'PayPal'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid_up_until': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['crm.CRMPerson']", 'unique': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['crm']