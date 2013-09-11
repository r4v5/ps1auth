# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    """ This migration is an add an id field to the PS1 User model.  The catch 
    is that it's using an existing column (object_guid) so we don't want to try
    and add a column that already exists
    """

    def forwards(self, orm):
        pass


    def backwards(self, orm):
        pass


    models = {
        u'accounts.ps1user': {
            'Meta': {'object_name': 'PS1User'},
            'id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '48', 'primary_key': True, 'db_column': "'object_guid'", 'db_index': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'object_guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '48', 'primary_key': 'True', 'db_index': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'accounts.token': {
            'Meta': {'object_name': 'Token'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'061af369-67bf-47c6-999f-8ea695900cac'", 'max_length': '36'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.PS1User']"})
        }
    }

    complete_apps = ['accounts']
