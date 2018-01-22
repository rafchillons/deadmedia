# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from deadsource.utils.download_and_save_module import download_and_save_file
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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_videos_page_old(request, filter_dict):
    try:
        page = int(request.GET.get('page', -1))
    except Exception as e:
        logging.error('error!{} '.format(e))
        page = -1

    all_videos = Video.objects.all().filter(**filter_dict).order_by('added_date')

    if page == -1:
        page = all_videos.__len__() / 24

    if 24 * (page - 1) - 24 >= 0:
        videos_to_show = all_videos[24 * (page - 1) - 24:(24 * page)]
    else:
        videos_to_show = all_videos[:24]

    for video in videos_to_show:
        video.is_liked = video.check_if_liked(request)

    list_of_grouped_videos = zip(*[iter(reversed(videos_to_show))] * 4)

    paginator = Paginator(list_of_grouped_videos, 6)

    try:
        videos = paginator.page(1)
        next_page = page - 1
        videos.next_page_number = next_page
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return videos


def get_videos_page(request, filter_dict, order_by='added_date'):
    try:
        page = int(request.GET.get('page', -2))
    except Exception as e:
        logging.error('error!{} '.format(e))
        page = -2

    if page == -2:
        paginator = Paginator([], 1)
        videos = paginator.page(paginator.num_pages)
        videos.next_page_number = -1
        videos.number = 0
        return videos

    all_videos = Video.objects.all().filter(**filter_dict).order_by('added_date')

    if page == -1:
        page = all_videos.__len__() / 24

    if 24 * (page - 1) - 24 >= 0:
        videos_to_show = all_videos[24 * (page - 1) - 24:(24 * page)]
    else:
        videos_to_show = all_videos[:24]

    for video in videos_to_show:
        video.is_liked = video.check_if_liked(request)

    list_of_grouped_videos = zip(*[iter(reversed(videos_to_show))] * 4)

    paginator = Paginator(list_of_grouped_videos, 6)

    try:
        videos = paginator.page(1)
        next_page = page - 1
        videos.next_page_number = next_page
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return videos


def get_filtered_and_sorted_videos_page(request, filter_dict, order_by='added_date'):
    try:
        page = int(request.GET.get('page', -2))
    except Exception as e:
        logging.error('error!{} '.format(e))
        page = -2

    if page == -2:
        paginator = Paginator([], 1)
        videos = paginator.page(paginator.num_pages)
        videos.next_page_number = -1
        videos.number = 0
        return videos

    all_videos = Video.objects.all().filter(**filter_dict).order_by(order_by)

    if page == -1:
        page = all_videos.__len__() / 24

    if 24 * (page - 1) - 24 >= 0:
        videos_to_show = all_videos[24 * (page - 1) - 24:(24 * page)]
    else:
        videos_to_show = all_videos[:24]

    for video in videos_to_show:
        video.is_liked = video.check_if_liked(request)

    list_of_grouped_videos = zip(*[iter(reversed(videos_to_show))] * 4)

    paginator = Paginator(list_of_grouped_videos, 6)

    try:
        videos = paginator.page(1)
        next_page = page - 1
        videos.next_page_number = next_page
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return videos

