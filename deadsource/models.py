# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

import threading
import json
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from .utils import hitcount_module
from django.shortcuts import render, redirect, get_object_or_404
import logging

class VideoViews(models.Model):
    pass


class VideoLikes(models.Model):
    pass


class VideoManager(models.Manager):
    def create_video(self):
        video_views = VideoViews()
        video_views.save()
        video_likes = VideoLikes()
        video_likes.save()
        video = self.create(video_likes_id=video_likes.id, video_views_id=video_views.id)
        return video


class Video(models.Model):
    objects = VideoManager()

    video_views_id = models.IntegerField()
    video_likes_id = models.IntegerField()

    title = models.CharField(max_length=200, default='Default title')

    added_date = models.DateTimeField(default=timezone.now)

    description_json = models.BinaryField(default=''.encode())

    storage_path = models.CharField(max_length=200, default='')
    storage_name = models.CharField(max_length=200, default='')
    storage_path_url = models.CharField(max_length=200, default='')

    source_path = models.CharField(max_length=200, default='')
    source_thread_number = models.CharField(max_length=200, default='')
    source_thread_path = models.CharField(max_length=200, default='')
    is_thread_alive = models.BooleanField(max_length=1, default=True)

    preview_storage_path = models.CharField(max_length=200, default='')
    preview_storage_name = models.CharField(max_length=200, default='')
    preview_storage_path_url = models.CharField(max_length=200, default='')

    video_width = models.CharField(max_length=200, default='300')
    video_height = models.CharField(max_length=200, default='300')

    video_size = models.CharField(max_length=200, default='0')

    video_size_str = models.CharField(max_length=200, default='0')
    video_duration_str = models.CharField(max_length=200, default='0')

    is_adult = models.BooleanField(max_length=1, default=False)
    is_music = models.BooleanField(max_length=1, default=False)
    is_hot = models.BooleanField(max_length=1, default=False)
    is_webm = models.BooleanField(max_length=1, default=False)
    is_mp4 = models.BooleanField(max_length=1, default=False)

    is_deleted = models.BooleanField(max_length=1, default=False)

    is_source_object_deleted = models.BooleanField(max_length=1, default=False)
    is_source_thread_deleted = models.BooleanField(max_length=1, default=False)

    STATUS_ERROR = 'Video status error'
    STATUS_NOTSET = 'Video status not set'
    STATUS_DOWNLOADING = 'Video is downloading'
    STATUS_DOWNLOADED = 'Video is downloaded'
    STATUS_DELETED = 'Video is deleted'
    STATUS_HIDDEN = 'Video is hidden'

    VIDEO_STATUS = (
        (STATUS_DOWNLOADING, 'Downloading'),
        (STATUS_DOWNLOADED, 'Downloaded'),
        (STATUS_NOTSET, 'Notset'),
        (STATUS_ERROR, 'Error'),
        (STATUS_HIDDEN, 'Hidden'),
        (STATUS_DELETED, 'Deleted'),
    )

    video_status = models.CharField(max_length=200, choices=VIDEO_STATUS, default=STATUS_NOTSET)

    FORMAT_MP4 = '.mp4'
    FORMAT_WEBM = '.webm'

    VIDEO_FORMATS = (
        (FORMAT_MP4, 'mp4'),
        (FORMAT_WEBM, 'webm'),
    )

    video_format = models.CharField(max_length=200, choices=VIDEO_FORMATS, default=FORMAT_WEBM)

    def __str__(self):
        return self.title

    def set_description(self, data):
        self.description_json = json.dumps(data)
        self.save()

    def get_description(self):
        return json.loads(str(self.description_json))

    @property
    def get_views(self):
        views = get_object_or_404(VideoViews, pk=self.video_views_id)
        hit_count = HitCount.objects.get_for_object(views)
        return hit_count.hits

    @property
    def get_likes(self):
        likes = get_object_or_404(VideoLikes, pk=self.video_likes_id)
        hit_count = HitCount.objects.get_for_object(likes)
        return hit_count.hits

    def view_video(self, request):
        views = get_object_or_404(VideoViews, pk=self.video_views_id)
        hit_count = HitCount.objects.get_for_object(views)
        hit_count_response = HitCountMixin.hit_count(request, hit_count)
        return hit_count_response.hit_counted

    def like_video(self, request):
        likes = get_object_or_404(VideoLikes, pk=self.video_likes_id)
        hit_count = HitCount.objects.get_for_object(likes)
        hit_count_response = HitCountMixin.hit_count(request, hit_count)
        return hit_count_response.hit_counted

    def check_if_liked(self, request):
        likes = get_object_or_404(VideoLikes, pk=self.video_likes_id)
        hit_count = HitCount.objects.get_for_object(likes)
        hit_count_response = hitcount_module.is_hit(request, hit_count)
        return not hit_count_response.hit_counted

    is_liked = models.BooleanField(max_length=1, default=False)

    def delete(self):
        try:
            likes = get_object_or_404(VideoLikes, pk=self.video_likes_id)
        except Exception as e:
            logging.error(e)
            likes = None

        try:
            views = get_object_or_404(VideoViews, pk=self.video_views_id)
        except Exception as e:
            logging.error(e)
            views = None

        super(Video, self).delete()

        if likes:
            likes.delete()

        if views:
            views.delete()



    """
    created_date = models.DateTimeField(
            default=timezone.now)

    downloaded_url = models.CharField(max_length=200)

    video = models.BinaryField()

    src_webm = models.CharField(max_length=200)

    FORMAT_WEBM = 'webm'
    FORMAT_MP4 = 'mp4'
    FORMAT_NOTSET = 'Format not set'
    FORMAT_UNKNOWN = 'Unknown video format'

    VIDEO_FORMATS = (
        (FORMAT_WEBM, 'webm'),
        (FORMAT_MP4, 'mp4'),
        (FORMAT_NOTSET, 'Notset'),
        (FORMAT_UNKNOWN, 'Unknown'),
    )

    STATUS_NOTSET = 'Status not set'
    STATUS_LINK_FOUND = 'Video is found and ready to download'
    STATUS_DOWNLOADING = 'Video is downloading'
    STATUS_DOWNLOADED = 'Video is downloaded'
    STATUS_READY = 'Video is ready to work'
    STATUS_FAIL = 'Video failed'
    STATUS_DELETED = 'Video deleted'

    VIDEO_STATUS = (
        (STATUS_NOTSET, 'Notset'),
        (STATUS_LINK_FOUND, 'Found'),
        (STATUS_DOWNLOADING, 'Downloading'),
        (STATUS_DOWNLOADED, 'Downloaded'),
        (STATUS_READY, 'Ready'),
        (STATUS_FAIL, 'Fail'),
        (STATUS_DELETED, 'Deleted'),
    )

    LINK_STATUS_NOTSET = 'Link status not set'
    LINK_STATUS_READY = 'Link is ready'
    LINK_STATUS_DELETED = 'Link is deleted'
    LINK_STATUS_BAD = 'Link is bad'

    LINK_STATUS = (
        (LINK_STATUS_NOTSET, 'Notset'),
        (LINK_STATUS_READY, 'Ready'),
        (LINK_STATUS_DELETED, 'Deleted'),
        (LINK_STATUS_BAD, 'Bad'),
    )


    video_format = models.CharField(max_length=200, choices=VIDEO_FORMATS)

    video_status = models.CharField(max_length=200, choices=VIDEO_STATUS)

    error_massage = models.CharField(max_length=200)

    def publish(self):
        self.published_date = timezone.now()
        self.save()


"""


class BotTask(models.Model):
    added_date = models.DateTimeField(default=timezone.now)

    BOT_STATUS_WORKING = 'working'
    BOT_STATUS_FINISHING = 'finishing'
    BOT_STATUS_STOPPED = 'stopped'

    BOT_STATUS = (
        (BOT_STATUS_WORKING, 'Working'),
        (BOT_STATUS_FINISHING, 'Finishing'),
        (BOT_STATUS_STOPPED, 'Stopped')
    )

    bot_status = models.CharField(max_length=200, choices=BOT_STATUS, default=BOT_STATUS_STOPPED)

    BOT_TASK_DOWNLOAD_2CH_WEBM = 'Download webms from 2ch'
    BOT_TASK_REMOVE_WEBM = 'Remove webms'
    BOT_TASK_INSPECT_BANNED = 'Insect banned'

    BOT_TASK = (
        (BOT_TASK_DOWNLOAD_2CH_WEBM, 'Download'),
        (BOT_TASK_REMOVE_WEBM, 'Remove'),
        (BOT_TASK_INSPECT_BANNED, 'Inspect')
    )

    bot_task = models.CharField(max_length=200, choices=BOT_TASK, default=BOT_TASK_DOWNLOAD_2CH_WEBM)

    task_data = models.BinaryField(default='{}')

    def start_bot(self):
        from .utils.bot_module import BotIsBusy, bot_task_1, bot_task_2, bot_task_3, TaskThread
        if filter(lambda x: x.getName() == 'Bot({})'.format(self.id), threading.enumerate()):
            raise BotIsBusy('Bot (id={}) is working already!'.format(self.id))

        data = json.loads(str(self.task_data))
        task = None
        if self.bot_task == self.BOT_TASK_DOWNLOAD_2CH_WEBM:
            task = bot_task_1
        elif self.bot_task == self.BOT_TASK_REMOVE_WEBM:
            task = bot_task_2
        elif self.bot_task == self.BOT_TASK_INSPECT_BANNED:
            task = bot_task_3()

        thread = TaskThread('Bot({})'.format(self.id), task, data)
        thread.start()
        self.bot_status = self.BOT_STATUS_WORKING
        self.save()

    def stop_bot(self):
        for thread in [x for x in threading.enumerate() if x.getName() == 'Bot({})'.format(self.id)]:
            thread.stop()

    @property
    def get_status(self):
        if not filter(lambda x: x.getName() == 'Bot({})'.format(self.id), threading.enumerate()):
            from .utils.bot_module import TaskThread
            return TaskThread.STATUS_STOPPED

        return list(filter(lambda x: x.getName() == 'Bot({})'.format(self.id),
                           threading.enumerate()))[0].get_status()

    @property
    def get_process_status(self):
        if not filter(lambda x: x.getName() == 'Bot({})'.format(self.id), threading.enumerate()):
            from .utils.bot_module import TaskThread
            return TaskThread.PROCESS_STATUS_RESTING

        return list(filter(lambda x: x.getName() == 'Bot({})'.format(self.id),
                           threading.enumerate()))[0].get_process_status()

    def pause_on(self):
        for thread in [x for x in threading.enumerate() if x.getName() == 'Bot({})'.format(self.id)]:
            thread.pause_on()

    def pause_off(self):
        for thread in [x for x in threading.enumerate() if x.getName() == 'Bot({})'.format(self.id)]:
            thread.pause_off()


class PaginatorModel(models.Model):
    updated_date = models.DateTimeField(default=timezone.now)

    paginator_json = models.BinaryField(default='')

    CATEGORY_HOT = 'Hot category'
    CATEGORY_ADULT = 'Adult category'
    CATEGORY_WEBM = 'Webm category'
    CATEGORY_MP4 = 'Mp4 category'
    CATEGORY_NOTSET = 'Category notset'
    
    CATEGORY = (
        (CATEGORY_HOT, 'hot'),
        (CATEGORY_ADULT, 'adult'),
        (CATEGORY_WEBM, 'webm'),
        (CATEGORY_MP4, 'mp4'),
        (CATEGORY_NOTSET, 'notset'),
    )

    category = models.CharField(max_length=200, choices=CATEGORY, default=CATEGORY_NOTSET)
    
    def set_paginator(self, data):
        self.paginator_json = json.dumps(data)
        self.save()

    def get_paginator(self):
        return json.loads(str(self.paginator_json))

    def __str__(self):
        return "Paginator model object ({})".format(self.category)



