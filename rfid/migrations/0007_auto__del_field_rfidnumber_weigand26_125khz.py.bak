# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'RFIDNumber.weigand26_125khz'
        db.delete_column(u'rfid_rfidnumber', 'weigand26_125khz')


    def backwards(self, orm):
        # Adding field 'RFIDNumber.weigand26_125khz'
        db.add_column(u'rfid_rfidnumber', 'weigand26_125khz',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=7, unique=True),
                      keep_default=False)


    models = {
        u'accounts.ps1user': {
            'Meta': {'object_name': 'PS1User'},
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'object_guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '48', 'primary_key': 'True', 'db_index': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'rfid.adgroupresource': {
            'Meta': {'object_name': 'AdGroupResource', '_ormbases': [u'rfid.Resource']},
            'ad_group': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'resource_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['rfid.Resource']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'rfid.resource': {
            'Meta': {'object_name': 'Resource'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '160'})
        },
        u'rfid.rfidnumber': {
            'ASCII_125khz': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '12'}),
            'Meta': {'object_name': 'RFIDNumber'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['accounts.PS1User']", 'unique': 'True'})
        }
    }

    complete_apps = ['rfid']