# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member_management', '0004_auto_20141228_1113'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='address_2',
            new_name='unit_number',
        ),
    ]
