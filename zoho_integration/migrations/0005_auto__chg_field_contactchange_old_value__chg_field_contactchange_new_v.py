# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ContactChange.old_value'
        db.alter_column(u'zoho_integration_contactchange', 'old_value', self.gf('django.db.models.fields.CharField')(max_length=300, null=True))

        # Changing field 'ContactChange.new_value'
        db.alter_column(u'zoho_integration_contactchange', 'new_value', self.gf('django.db.models.fields.CharField')(max_length=300, null=True))

    def backwards(self, orm):

        # Changing field 'ContactChange.old_value'
        db.alter_column(u'zoho_integration_contactchange', 'old_value', self.gf('django.db.models.fields.CharField')(default='None', max_length=300))

        # Changing field 'ContactChange.new_value'
        db.alter_column(u'zoho_integration_contactchange', 'new_value', self.gf('django.db.models.fields.CharField')(default='None', max_length=300))

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
            'membership_end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
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
            'new_value': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '300', 'null': 'True'}),
            'old_value': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '300', 'null': 'True'})
        },
        u'zoho_integration.token': {
            'Meta': {'object_name': 'Token'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'zoho_contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['zoho_integration.Contact']"})
        }
    }

    complete_apps = ['zoho_integration']