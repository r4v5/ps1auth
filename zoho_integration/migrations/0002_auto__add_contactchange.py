# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ContactChange'
        db.create_table(u'zoho_integration_contactchange', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['zoho_integration.Contact'])),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('detected_on', self.gf('django.db.models.fields.DateTimeField')()),
            ('old_value', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('new_value', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'zoho_integration', ['ContactChange'])


    def backwards(self, orm):
        # Deleting model 'ContactChange'
        db.delete_table(u'zoho_integration_contactchange')


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
        u'zoho_integration.contactchange': {
            'Contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['zoho_integration.Contact']"}),
            'Meta': {'object_name': 'ContactChange'},
            'detected_on': ('django.db.models.fields.DateTimeField', [], {}),
            'field': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_value': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'old_value': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'zoho_integration.token': {
            'Meta': {'object_name': 'Token'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'zoho_contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['zoho_integration.Contact']"})
        }
    }

    complete_apps = ['zoho_integration']