# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-06 15:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deadsource', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='is_adult',
            field=models.BooleanField(default=False, max_length=1),
        ),
    ]
