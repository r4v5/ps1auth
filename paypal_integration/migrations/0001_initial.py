# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Transaction'
        db.create_table(u'paypal_integration_transaction', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=30, primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('amount_currency', self.gf('djmoney.models.fields.CurrencyField')()),
            ('amount', self.gf('djmoney.models.fields.MoneyField')(max_digits=10, decimal_places=2, default_currency='XYZ')),
            ('fee_amount_currency', self.gf('djmoney.models.fields.CurrencyField')()),
            ('fee_amount', self.gf('djmoney.models.fields.MoneyField')(max_digits=10, decimal_places=2, default_currency='XYZ')),
            ('net_amount_currency', self.gf('djmoney.models.fields.CurrencyField')()),
            ('net_amount', self.gf('djmoney.models.fields.MoneyField')(max_digits=10, decimal_places=2, default_currency='XYZ')),
        ))
        db.send_create_signal(u'paypal_integration', ['Transaction'])


    def backwards(self, orm):
        # Deleting model 'Transaction'
        db.delete_table(u'paypal_integration_transaction')


    models = {
        u'paypal_integration.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'amount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': u"'XYZ'"}),
            'amount_currency': ('djmoney.models.fields.CurrencyField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fee_amount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': u"'XYZ'"}),
            'fee_amount_currency': ('djmoney.models.fields.CurrencyField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'net_amount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': u"'XYZ'"}),
            'net_amount_currency': ('djmoney.models.fields.CurrencyField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['paypal_integration']