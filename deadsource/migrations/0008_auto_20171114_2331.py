# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-14 23:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deadsource', '0007_video_is_mp4'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='is_deleted',
            field=models.BooleanField(default=False, max_length=1),
        ),
        migrations.AddField(
            model_name='video',
            name='is_source_object_deleted',
            field=models.BooleanField(default=False, max_length=1),
        ),
        migrations.AddField(
            model_name='video',
            name='is_source_thread_deleted',
            field=models.BooleanField(default=False, max_length=1),
        ),
    ]
