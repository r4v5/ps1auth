# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Transaction.email'
        db.delete_column('paypal_integration_transaction', 'email')

        # Adding field 'Transaction.from_email'
        db.add_column('paypal_integration_transaction', 'from_email',
                      self.gf('django.db.models.fields.EmailField')(default='', max_length=75),
                      keep_default=False)

        # Adding field 'Transaction.to_email'
        db.add_column('paypal_integration_transaction', 'to_email',
                      self.gf('django.db.models.fields.EmailField')(default='', max_length=75),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Transaction.email'
        db.add_column('paypal_integration_transaction', 'email',
                      self.gf('django.db.models.fields.EmailField')(default='', max_length=75),
                      keep_default=False)

        # Deleting field 'Transaction.from_email'
        db.delete_column('paypal_integration_transaction', 'from_email')

        # Deleting field 'Transaction.to_email'
        db.delete_column('paypal_integration_transaction', 'to_email')


    models = {
        'paypal_integration.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'amount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'XYZ'"}),
            'amount_currency': ('djmoney.models.fields.CurrencyField', [], {}),
            'balance': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'XYZ'"}),
            'balance_currency': ('djmoney.models.fields.CurrencyField', [], {}),
            'fee_amount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'XYZ'"}),
            'fee_amount_currency': ('djmoney.models.fields.CurrencyField', [], {}),
            'from_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'net_amount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'XYZ'"}),
            'net_amount_currency': ('djmoney.models.fields.CurrencyField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'to_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['paypal_integration']