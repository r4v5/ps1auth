# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memberpoint', '0002_auto_20141213_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberpoint',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
