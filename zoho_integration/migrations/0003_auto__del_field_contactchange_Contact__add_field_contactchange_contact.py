# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ContactChange.Contact'
        db.delete_column(u'zoho_integration_contactchange', 'Contact_id')

        # Adding field 'ContactChange.contact'
        db.add_column(u'zoho_integration_contactchange', 'contact',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['zoho_integration.Contact']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'ContactChange.Contact'
        db.add_column(u'zoho_integration_contactchange', 'Contact',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['zoho_integration.Contact']),
                      keep_default=False)

        # Deleting field 'ContactChange.contact'
        db.delete_column(u'zoho_integration_contactchange', 'contact_id')


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
            'Meta': {'object_name': 'ContactChange'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['zoho_integration.Contact']"}),
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