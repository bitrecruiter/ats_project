# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ats_profiles', '0002_auto_20140925_1058'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='attached_files',
            field=models.ManyToManyField(to='ats_profiles.UserProfileAttachedFile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='tags',
            field=models.ManyToManyField(to=b'ats_profiles.Tag'),
        ),
    ]
