# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class Video(models.Model):
    title = models.CharField(max_length=200, default='Default title')

    added_date = models.DateTimeField(default=timezone.now)

    description_json = models.BinaryField(default='')

    storage_path = models.CharField(max_length=200, default='')
    storage_name = models.CharField(max_length=200, default='')

    source_path = models.CharField(max_length=200, default='')

    preview_storage_path = models.CharField(max_length=200, default='')
    preview_storage_name = models.CharField(max_length=200, default='')

    video_width = models.CharField(max_length=200, default='300')
    video_height = models.CharField(max_length=200, default='300')

    video_size = models.CharField(max_length=200, default='0')

    video_size_str = models.CharField(max_length=200, default='0')
    video_duration_str = models.CharField(max_length=200, default='0')

    STATUS_NOTSET = 'Video status not set'
    STATUS_DOWNLOADING = 'Video is downloading'
    STATUS_DOWNLOADED = 'Video is downloaded'

    VIDEO_STATUS = (
        (STATUS_DOWNLOADING, 'Downloading'),
        (STATUS_DOWNLOADED, 'Downloaded'),
        (STATUS_NOTSET, 'Notset')
    )

    video_status = models.CharField(max_length=200, choices=VIDEO_STATUS, default=STATUS_NOTSET)

    def __str__(self):
        return self.title

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