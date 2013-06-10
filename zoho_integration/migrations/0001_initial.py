# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Contact'
        db.create_table(u'zoho_integration_contact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('membership_status', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('modified_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['accounts.PS1User'], unique=True, null=True)),
        ))
        db.send_create_signal(u'zoho_integration', ['Contact'])

        # Adding model 'Token'
        db.create_table(u'zoho_integration_token', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('zoho_contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['zoho_integration.Contact'])),
        ))
        db.send_create_signal(u'zoho_integration', ['Token'])


    def backwards(self, orm):
        # Deleting model 'Contact'
        db.delete_table(u'zoho_integration_contact')

        # Deleting model 'Token'
        db.delete_table(u'zoho_integration_token')


    models = {
        u'accounts.ps1user': {
            'Meta': {'object_name': 'PS1User'},
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'object_guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '48', 'primary_key': 'True', 'db_index': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'zoho_integration.contact': {
            'Meta': {'object_name': 'Contact'},
            'contact_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'membership_status': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'modified_time': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['accounts.PS1User']", 'unique': 'True', 'null': 'True'})
        },
        u'zoho_integration.token': {
            'Meta': {'object_name': 'Token'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'zoho_contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['zoho_integration.Contact']"})
        }
    }

    complete_apps = ['zoho_integration']