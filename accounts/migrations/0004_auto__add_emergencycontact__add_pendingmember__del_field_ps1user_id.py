# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EmergencyContact'
        db.create_table(u'accounts_emergencycontact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.PendingMember'])),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phone_number', self.gf('localflavor.us.models.PhoneNumberField')(max_length=20)),
            ('relationship', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'accounts', ['EmergencyContact'])

        # Adding model 'PendingMember'
        db.create_table(u'accounts_pendingmember', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('phone_number', self.gf('localflavor.us.models.PhoneNumberField')(max_length=20)),
            ('street_address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('second_address_line', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(default='Chicago', max_length=255)),
            ('state', self.gf('localflavor.us.models.USPostalCodeField')(default='IL', max_length=2)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(max_length=255)),
        ))
        db.send_create_signal(u'accounts', ['PendingMember'])

    def backwards(self, orm):
        # Deleting model 'EmergencyContact'
        db.delete_table(u'accounts_emergencycontact')

        # Deleting model 'PendingMember'
        db.delete_table(u'accounts_pendingmember')
        
    models = {
        u'accounts.emergencycontact': {
            'Meta': {'object_name': 'EmergencyContact'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.PendingMember']"}),
            'phone_number': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'relationship': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'accounts.pendingmember': {
            'Meta': {'object_name': 'PendingMember'},
            'city': ('django.db.models.fields.CharField', [], {'default': "'Chicago'", 'max_length': '255'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'phone_number': ('localflavor.us.models.PhoneNumberField', [], {'max_length': '20'}),
            'second_address_line': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'state': ('localflavor.us.models.USPostalCodeField', [], {'default': "'IL'", 'max_length': '2'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'accounts.ps1user': {
            'Meta': {'object_name': 'PS1User'},
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'object_guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '48', 'primary_key': 'True', 'db_index': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'accounts.token': {
            'Meta': {'object_name': 'Token'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'598d7e95-1978-448c-ae25-c867d9f455ba'", 'max_length': '36'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.PS1User']"})
        }
    }

    complete_apps = ['accounts']
