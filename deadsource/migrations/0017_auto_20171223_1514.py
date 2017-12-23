# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-23 15:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deadsource', '0016_auto_20171223_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='video_status',
            field=models.CharField(choices=[('Video is downloading', 'Downloading'), ('Video is downloaded', 'Downloaded'), ('Video status not set', 'Notset'), ('Video status error', 'Error'), ('Video is hidden', 'Hidden'), ('Video is deleted', 'Deleted')], default='Video status not set', max_length=200),
        ),
    ]