# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('member_management', '0002_note_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idcheck',
            name='user',
            field=models.ForeignKey(help_text=b'Only Board Members are able to perform ID checks.', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
