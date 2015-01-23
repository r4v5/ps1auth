# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('member_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact_id', models.BigIntegerField(unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=300)),
                ('membership_status', models.CharField(max_length=300, choices=[(b'Full', b'Full Membership'), (b'Starving', b'Starving Hacker')])),
                ('modified_time', models.DateTimeField()),
                ('membership_end_date', models.DateField(null=True, blank=True)),
                ('user', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.CharField(max_length=300)),
                ('detected_on', models.DateTimeField()),
                ('old_value', models.CharField(default=b'None', max_length=300, null=True)),
                ('new_value', models.CharField(default=b'None', max_length=300, null=True)),
                ('contact', models.ForeignKey(to='zoho_integration.Contact')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=36)),
                ('zoho_contact', models.ForeignKey(to='member_management.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
