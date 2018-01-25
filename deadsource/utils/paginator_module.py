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


def get_filtered_and_sorted_videos_page_old2(request, filter_dict, order_by='added_date'):

    all_videos = Video.objects.all().filter(**filter_dict).order_by(order_by)

    try:
        print('first:{}'.format(request.GET.get('first', -1)))
        page = int(request.GET.get('page', -1))
    except Exception as e:
        raise
        logging.error('error!{} '.format(e))
        page = -1

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


def get_filtered_and_sorted_videos_page_old(request, filter_dict, order_by='added_date'):
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


def get_filtered_and_sorted_videos_page(request, filter_dict, order_by='added_date'):

    all_videos = Video.objects.all().filter(**filter_dict).order_by(order_by)
    all_videos_count = all_videos.__len__()

    if all_videos_count < 24:
        return []

    try:
        page = int(request.GET.get('page', -1))
        first = int(request.GET.get('first', -1))
        last = int(request.GET.get('last', -1))
        const = int(request.GET.get('const', 0))
    except Exception as e:
        logging.error('error!{} '.format(e))
        page, last, first = -1, -1, -1
        const = 0

    print('start: page:{}, first:{}, last:{}, const:{}'.format(
        page,
        first,
        last,
        const
    ))

    if page < 0 or first < 0:
        print('!111111111111!!!!!!!!!!!!!!!!!!!!!!!!!!')
        page = 0
        page_const = 0
        first_page_element = all_videos[0].id

    elif first != all_videos[0].id:

        print('!2222222222!!!!!!!!!!!!!!!!!!!!!!!!!!')
        first_page_element = all_videos[0].id

        for i, video in enumerate(all_videos):
            if video.id == first:
                page_const = i + const
                break
        else:
            page_const = const

    else:

        print('!3333333333!!!!!!!!!!!!!!!!!!!!!!!!!!')
        first_page_element = first
        page_const = const

    all_videos_count = all_videos_count - page_const

    first_element_number = 24 * page + page_const
    last_element_number = 24 + 24 * page + page_const

    print('mid: first_element_number:{}, last_element_number:{}, const:{}'.format(
        first_element_number,
        last_element_number,
        page_const))

    last_page_element = all_videos[last_element_number - 1].id

    try:
        videos_to_show = all_videos[first_element_number:last_element_number]
    except IndexError as e:
        logging.error(e)
        return []

    videos_to_show_dict = []
    for video in videos_to_show:
        videos_to_show_dict.append(
            {
                'views': video.video_views,
                'likes': video.video_likes,
                'status': video.video_status,
                'source_thread_number': video.source_thread_number,
                'source_thread_path': video.source_thread_path,
                'is_thread_alive': video.is_thread_alive,
                'added_date': video.added_date,
                'storage_path_url': video.storage_path_url,
                'preview_storage_path_url': video.preview_storage_path_url,
                'id': video.id,
                'title': video.title,
                'height': video.video_height,
                'width': video.video_width,
                'duration': video.video_duration_str,
                'size': video.video_size_str,
                'is_reported': video.check_if_reported(request),
                'is_liked': video.check_if_liked(request),
            }
        )

    list_of_grouped_videos = zip(*[iter(videos_to_show_dict)] * 4)

    videos = {
        'videos': list_of_grouped_videos,
        'next_page_number': page + 1,
        'first_page_element': first_page_element,
        'last_page_element': last_page_element,
        'page_const': page_const,
        'number': page,
        'num_pages': all_videos_count / 24 - 1,
    }

    videos['has_next'] = videos['number'] < videos['num_pages']
    print('end: next_page_number:{}, first_page_element:{}, last_page_element:{}, page_const:{}, number:{}, num_pages:{}, has_next:{}'.format(
        videos['next_page_number'],
        videos['first_page_element'],
        videos['last_page_element'],
        videos['page_const'],
        videos['number'],
        videos['num_pages'],
        videos['has_next'],
    ))
    return videos