# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-16 14:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deadsource', '0009_auto_20171115_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='video_format',
            field=models.CharField(choices=[('.mp4', '.mp4'), ('.webm', '.webm')], default='.webm', max_length=200),
        ),
    ]
