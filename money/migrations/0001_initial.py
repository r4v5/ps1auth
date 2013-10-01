# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Account'
        db.create_table(u'money_account', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'money', ['Account'])

        # Adding model 'UserAccount'
        db.create_table(u'money_useraccount', (
            (u'account_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['money.Account'], unique=True, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.PS1User'])),
        ))
        db.send_create_signal(u'money', ['UserAccount'])

        # Adding model 'Transaction'
        db.create_table(u'money_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'money', ['Transaction'])

        # Adding model 'MoneyTransaction'
        db.create_table(u'money_moneytransaction', (
            (u'transaction_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['money.Transaction'], unique=True, primary_key=True)),
            ('amount', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'money', ['MoneyTransaction'])

        # Adding model 'MemberPointTransaction'
        db.create_table(u'money_memberpointtransaction', (
            (u'transaction_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['money.Transaction'], unique=True, primary_key=True)),
            ('amount', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'money', ['MemberPointTransaction'])


    def backwards(self, orm):
        # Deleting model 'Account'
        db.delete_table(u'money_account')

        # Deleting model 'UserAccount'
        db.delete_table(u'money_useraccount')

        # Deleting model 'Transaction'
        db.delete_table(u'money_transaction')

        # Deleting model 'MoneyTransaction'
        db.delete_table(u'money_moneytransaction')

        # Deleting model 'MemberPointTransaction'
        db.delete_table(u'money_memberpointtransaction')


    models = {
        u'accounts.ps1user': {
            'Meta': {'object_name': 'PS1User'},
            'id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '48', 'primary_key': True, 'db_column': "'object_guid'", 'db_index': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'object_guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '48', 'primary_key': 'True', 'db_index': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'money.account': {
            'Meta': {'object_name': 'Account'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        u'money.memberpointtransaction': {
            'Meta': {'object_name': 'MemberPointTransaction', '_ormbases': [u'money.Transaction']},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            u'transaction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['money.Transaction']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'money.moneytransaction': {
            'Meta': {'object_name': 'MoneyTransaction', '_ormbases': [u'money.Transaction']},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            u'transaction_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['money.Transaction']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'money.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'money.useraccount': {
            'Meta': {'object_name': 'UserAccount', '_ormbases': [u'money.Account']},
            u'account_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['money.Account']", 'unique': 'True', 'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.PS1User']"})
        }
    }

    complete_apps = ['money']