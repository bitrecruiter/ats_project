# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ats_profiles', '0003_auto_20140925_1059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofileattachedfile',
            name='user',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address1',
            field=models.CharField(max_length=256, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address2',
            field=models.CharField(max_length=256, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='attached_files',
            field=models.ManyToManyField(to=b'ats_profiles.UserProfileAttachedFile', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(max_length=256, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='cvtext',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(max_length=256, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='postcode',
            field=models.CharField(max_length=32, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='salutation',
            field=models.CharField(blank=True, max_length=3, choices=[(b'Mr.', b'Mr.'), (b'Ms.', b'Ms.')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='summary',
            field=models.CharField(max_length=256, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='tags',
            field=models.ManyToManyField(to=b'ats_profiles.Tag', blank=True),
        ),
    ]
