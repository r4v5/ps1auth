# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memberpoint', '0003_auto_20141213_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberpoint',
            name='reason',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
