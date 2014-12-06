# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Transaction.balance_currency'
        db.add_column(u'paypal_integration_transaction', 'balance_currency',
                      self.gf('djmoney.models.fields.CurrencyField')(),
                      keep_default=False)

        # Adding field 'Transaction.balance'
        db.add_column(u'paypal_integration_transaction', 'balance',
                      self.gf('djmoney.models.fields.MoneyField')(max_digits=10, decimal_places=2, default_currency='XYZ'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Transaction.balance_currency'
        db.delete_column(u'paypal_integration_transaction', 'balance_currency')

        # Deleting field 'Transaction.balance'
        db.delete_column(u'paypal_integration_transaction', 'balance')


    models = {
        u'paypal_integration.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'amount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': u"'XYZ'"}),
            'amount_currency': ('djmoney.models.fields.CurrencyField', [], {}),
            'balance': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': u"'XYZ'"}),
            'balance_currency': ('djmoney.models.fields.CurrencyField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fee_amount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': u"'XYZ'"}),
            'fee_amount_currency': ('djmoney.models.fields.CurrencyField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'net_amount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': u"'XYZ'"}),
            'net_amount_currency': ('djmoney.models.fields.CurrencyField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['paypal_integration']