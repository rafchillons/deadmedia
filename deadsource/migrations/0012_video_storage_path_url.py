# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-24 22:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deadsource', '0011_auto_20171121_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='storage_path_url',
            field=models.CharField(default='', max_length=200),
        ),
    ]