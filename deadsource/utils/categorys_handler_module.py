# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from deadsource.utils.download_and_save_module import download_and_save_file
from deadsource.utils.video_handler_module import delete_video_by_db_object
from django.shortcuts import render, redirect, get_object_or_404
import json
from deadsource.utils import parse_2ch_module
from urllib2 import Request, urlopen
import urllib2
import threading
import logging
import time
from datetime import datetime
from deadsource.models import Video
from deadmedia.settings import MEDIA_ROOT, MEDIA_URL
from os.path import (
    join,
    basename,
)

from os import remove
import os


def remove_all_videos_from_category(category, video_status=Video.STATUS_DOWNLOADED):
    args = {'video_status': video_status, category: True}

    videos = Video.objects.all().filter(**args)
    for video in videos:
        video.__setattr__(category, False)
        video.save()


def delete_all_videos_with_category(category, video_status=Video.STATUS_DOWNLOADED):
    args = {'video_status': video_status, category: True}

    videos = Video.objects.all().filter(**args)
    for video in videos:
        delete_video_by_db_object(video)