# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word', models.CharField(max_length=35)),
                ('created_at', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('salutation', models.CharField(max_length=3, choices=[(b'Mr.', b'Mr.'), (b'Ms.', b'Ms.')])),
                ('address1', models.CharField(max_length=256)),
                ('address2', models.CharField(max_length=256)),
                ('city', models.CharField(max_length=256)),
                ('postcode', models.CharField(max_length=32)),
                ('phone', models.CharField(max_length=256)),
                ('summary', models.CharField(max_length=256)),
                ('cvtext', models.TextField()),
                ('tags', models.ManyToManyField(to='ats_profiles.Tag')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
