# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'RFIDNumber.weigand26_125khz'
        db.add_column('rfid_rfidnumber', 'weigand26_125khz',
                      self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=7),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'RFIDNumber.weigand26_125khz'
        db.delete_column('rfid_rfidnumber', 'weigand26_125khz')


    models = {
        'accounts.ps1user': {
            'Meta': {'object_name': 'PS1User'},
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'object_guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '48', 'primary_key': 'True', 'db_index': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'rfid.adgroupresource': {
            'Meta': {'object_name': 'AdGroupResource', '_ormbases': ['rfid.Resource']},
            'ad_group': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'resource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['rfid.Resource']", 'unique': 'True', 'primary_key': 'True'})
        },
        'rfid.resource': {
            'Meta': {'object_name': 'Resource'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '160'})
        },
        'rfid.rfidnumber': {
            'Meta': {'object_name': 'RFIDNumber'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['accounts.PS1User']", 'unique': 'True'}),
            'weigand26_125khz': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '7'})
        }
    }

    complete_apps = ['rfid']