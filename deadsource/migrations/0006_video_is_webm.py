# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-14 15:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deadsource', '0005_video_is_hot'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='is_webm',
            field=models.BooleanField(default=False, max_length=1),
        ),
    ]