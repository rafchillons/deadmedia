# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-24 20:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deadsource', '0019_auto_20171224_2017'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='VideoView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='video',
            name='video_likes',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='deadsource.VideoLike'),
        ),
        migrations.AddField(
            model_name='video',
            name='video_views',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='deadsource.VideoView'),
        ),
    ]