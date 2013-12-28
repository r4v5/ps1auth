# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Resource'
        db.create_table(u'rfid_resource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=160)),
        ))
        db.send_create_signal(u'rfid', ['Resource'])

        # Adding model 'RFIDNumber'
        db.create_table(u'rfid_rfidnumber', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['accounts.PS1User'], unique=True)),
            ('number', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
        ))
        db.send_create_signal(u'rfid', ['RFIDNumber'])


    def backwards(self, orm):
        # Deleting model 'Resource'
        db.delete_table(u'rfid_resource')

        # Deleting model 'RFIDNumber'
        db.delete_table(u'rfid_rfidnumber')


    models = {
        u'accounts.ps1user': {
            'Meta': {'object_name': 'PS1User'},
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'object_guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '48', 'primary_key': 'True', 'db_index': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'rfid.resource': {
            'Meta': {'object_name': 'Resource'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '160'})
        },
        u'rfid.rfidnumber': {
            'Meta': {'object_name': 'RFIDNumber'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['accounts.PS1User']", 'unique': 'True'})
        }
    }

    complete_apps = ['rfid']