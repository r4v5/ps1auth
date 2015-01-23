# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import ckeditor.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cash',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('paid_up_until', models.DateField(blank=True)),
            ],
            options={
                'verbose_name': 'cash',
                'verbose_name_plural': 'cash',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailAttachement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to=b'attachements/%Y/%m/%d')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=128)),
                ('message', models.TextField()),
                ('from_email', models.EmailField(max_length=75)),
                ('reply_to_email', models.EmailField(max_length=75, blank=True)),
                ('to_email', models.EmailField(max_length=75)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default=b'pending', max_length=30)),
            ],
            options={
                'ordering': ['-created_at'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_name', models.CharField(max_length=255, blank=True)),
                ('from_email', models.EmailField(max_length=75, verbose_name=b'From')),
                ('reply_to_name', models.CharField(max_length=255, blank=True)),
                ('reply_to_email', models.EmailField(max_length=75, verbose_name=b'Reply-To', blank=True)),
                ('recipients', models.CharField(default=b'full_members', max_length=128, choices=[(b'all_members', b'All Members'), (b'full_members', b'Full Members'), (b'individual', b'Individual')])),
                ('subject', models.CharField(max_length=128)),
                ('message', ckeditor.fields.RichTextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IDCheck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.TextField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PayPal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75)),
                ('paid_up_until', models.DateField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'PayPal',
                'verbose_name_plural': 'PayPal',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('birthday', models.DateField(null=True, blank=True)),
                ('membership_status', models.CharField(default=b'discontinued', max_length=128, choices=[(b'discontinued', b'Discontinued'), (b'starving_hacker', b'Starving Hacker'), (b'full_member', b'Full Member'), (b'suspended', b'Suspended'), (b'banned', b'Banned')])),
                ('membership_start_date', models.DateField(default=datetime.date.today)),
                ('street_address', models.CharField(max_length=128, null=True, blank=True)),
                ('city', models.CharField(max_length=128, null=True, blank=True)),
                ('zip_code', models.CharField(max_length=128, null=True, blank=True)),
                ('country', models.CharField(max_length=128, null=True, blank=True)),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='paypal',
            name='person',
            field=models.OneToOneField(null=True, to='member_management.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='note',
            name='person',
            field=models.ForeignKey(to='member_management.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='idcheck',
            name='person',
            field=models.ForeignKey(to='member_management.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='idcheck',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emailrecord',
            name='recipient',
            field=models.ForeignKey(to='member_management.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emailrecord',
            name='sender',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emailattachement',
            name='email',
            field=models.ForeignKey(related_name='attachments', to='member_management.EmailTemplate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cash',
            name='person',
            field=models.OneToOneField(null=True, to='member_management.Person'),
            preserve_default=True,
        ),
    ]
