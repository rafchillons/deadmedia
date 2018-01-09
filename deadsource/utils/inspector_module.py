# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from deadsource.utils.download_and_save_module import download_and_save_file
from deadsource.utils.parse_2ch_module import _download_from_url, _find_files_in_thread
from django.shortcuts import render, redirect, get_object_or_404
import json
from deadsource.utils import parse_2ch_module
from urllib2 import Request, urlopen, HTTPError
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


def fined_banned_videos_and_delete_them():
    threads_to_check = _get_threads_to_check()
    banned_videos = _fined_banned_videos(threads_to_check)
    _delete_banned_videos(banned_videos)


def _get_threads_to_check():
    videos_to_check = Video.objects.filter(video_status=Video.STATUS_DOWNLOADED, is_thread_alive=True)

    threads = set([x.source_thread_number for x in videos_to_check])
    threads_and_videos = {x:[] for x in threads}
    for video in videos_to_check:
        threads_and_videos[video.source_thread_number].append(video)

    return threads_and_videos


def _fined_banned_videos(thread_to_check):
    banned_videos = []

    for thread in thread_to_check:
        try:
            founded_files = _find_files_in_thread('https://2ch.hk/b/res/{}.json'.format(thread))
            founded_paths = [x['path'] for x in founded_files]

            banned_videos_in_thread = []

            for video in thread_to_check[thread]:
                if json.loads(video.description_json.decode('utf-8'))['path'] not in founded_paths:
                    banned_videos.append(video)

            _find_files_in_thread('https://2ch.hk/b/res/{}.json'.format(thread))

            banned_videos.extend(banned_videos_in_thread)
        except HTTPError as e:
            for video in thread_to_check[thread]:
                video.is_thread_alive = False
                video.save()

    return banned_videos


def _delete_banned_videos(banned_videos):
    for video in banned_videos:
        video.video_status = Video.STATUS_HIDDEN
        video.save()


