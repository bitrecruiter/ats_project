# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.CharField(max_length=256)),
                ('job_title', models.CharField(max_length=256)),
                ('apply_identifier', models.CharField(max_length=256)),
                ('job_description', models.TextField()),
                ('location', models.CharField(max_length=256)),
                ('contact_email', models.EmailField(max_length=254)),
                ('reference_number', models.CharField(max_length=256)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
