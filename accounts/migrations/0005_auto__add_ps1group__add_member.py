# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PS1Group'
        db.create_table(u'accounts_ps1group', (
            ('object_guid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=48, primary_key=True, db_index=True)),
        ))
        db.send_create_signal(u'accounts', ['PS1Group'])

        # Adding M2M table for field permissions on 'PS1Group'
        m2m_table_name = db.shorten_name(u'accounts_ps1group_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ps1group', models.ForeignKey(orm[u'accounts.ps1group'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['ps1group_id', 'permission_id'])

        # Adding model 'Member'
        db.create_table(u'accounts_member', (
            (u'pendingmember_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['accounts.PendingMember'], unique=True, primary_key=True)),
            ('object_guid', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['accounts.PS1User'], unique=True)),
        ))
        db.send_create_signal(u'accounts', ['Member'])


    def backwards(self, orm):
        # Deleting model 'PS1Group'
        db.delete_table(u'accounts_ps1group')

        # Removing M2M table for field permissions on 'PS1Group'
        db.delete_table(db.shorten_name(u'accounts_ps1group_permissions'))

        # Deleting model 'Member'
        db.delete_table(u'accounts_member')


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
            'object_guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '48', 'primary_key': 'True', 'db_index': 'True'}),
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
            'key': ('django.db.models.fields.CharField', [], {'default': "'2bb92c7c-4dd0-4fed-bc80-308ea040ceb9'", 'max_length': '36'}),
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