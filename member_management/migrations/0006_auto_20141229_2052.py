# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('member_management', '0005_auto_20141228_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 30, 2, 52, 16, 747989, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='updated_on',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 30, 2, 52, 20, 291183, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
