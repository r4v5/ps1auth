# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    
    depends_on = (
        ("member_management", "0001_initial"),
    )

    def forwards(self, orm):

        # Changing field 'Token.zoho_contact'
        db.alter_column(u'zoho_integration_token', 'zoho_contact_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['member_management.Person']))

    def backwards(self, orm):

        # Changing field 'Token.zoho_contact'
        db.alter_column(u'zoho_integration_token', 'zoho_contact_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['zoho_integration.Contact']))

    models = {
        u'accounts.ps1user': {
            'Meta': {'object_name': 'PS1User'},
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'object_guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '48', 'primary_key': 'True', 'db_index': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
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
            'zoho_contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['member_management.Person']"})
        }
    }

    complete_apps = ['zoho_integration']
