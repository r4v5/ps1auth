# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'PS1Group.object_guid'
        db.delete_column(u'accounts_ps1group', 'object_guid')

        # Adding field 'PS1Group.group_dn'
        db.add_column(u'accounts_ps1group', 'group_dn',
                      self.gf('django.db.models.fields.CharField')(default='invalid_data', unique=True, max_length=255, primary_key=True, db_index=True),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'PS1Group.object_guid'
        raise RuntimeError("Cannot reverse this migration. 'PS1Group.object_guid' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'PS1Group.object_guid'
        db.add_column(u'accounts_ps1group', 'object_guid',
                      self.gf('django.db.models.fields.CharField')(max_length=48, unique=True, primary_key=True, db_index=True),
                      keep_default=False)

        # Deleting field 'PS1Group.group_dn'
        db.delete_column(u'accounts_ps1group', 'group_dn')


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
        u'accounts.member': {
            'Meta': {'object_name': 'Member', '_ormbases': [u'accounts.PendingMember']},
            'object_guid': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['accounts.PS1User']", 'unique': 'True'}),
            u'pendingmember_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['accounts.PendingMember']", 'unique': 'True', 'primary_key': 'True'})
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
        u'accounts.ps1group': {
            'Meta': {'object_name': 'PS1Group'},
            'group_dn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'primary_key': 'True', 'db_index': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False'})
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
            'key': ('django.db.models.fields.CharField', [], {'default': "'aaab641a-7221-4c81-bf73-d25aff346f61'", 'max_length': '36'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.PS1User']"})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['accounts']