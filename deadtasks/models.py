# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class DownloadDvachTask(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    last_launch_date = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=False)

    download_format_webm = models.BooleanField(default=True)
    download_format_mp4 = models.BooleanField(default=False)

    required_words = models.CharField(max_length=50, default="")
    banned_words = models.CharField(max_length=50, default="")

    CATEGORY_HOT = 0
    CATEGORY_WEBM = 1
    CATEGORY_MP4 = 2
    CATEGORY_ADULT = 3

    VIDEO_CATEGORIES = (
        (CATEGORY_HOT, 'hot'),
        (CATEGORY_WEBM, 'webm'),
        (CATEGORY_MP4, 'mp4'),
        (CATEGORY_ADULT, 'adult'),
    )

    video_category = models.IntegerField(choices=VIDEO_CATEGORIES)

    @property
    def get_required_words_list(self):
        return self.required_words.split()

    @property
    def get_banned_words_list(self):
        return self.banned_words.split()

    @property
    def get_formats_to_download_list(self):
        result = []

        if self.download_format_webm:
            result.append('.webm')
        if self.download_format_mp4:
            result.append('.mp4')

        return result

    @property
    def get_video_category(self):
        for pair in self.VIDEO_CATEGORIES:
            if pair[0] == self.video_category:
                return pair[1]

    def activate(self):
        if self.is_active is not True:
            self.is_active = True
            self.save()

    def deactivate(self):
        if self.is_active is True:
            self.is_active = False
            self.save()

    def update_last_launch_date(self):
        self.last_launch_date = str(timezone.now())
        self.save()


class RemoveOldTask(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    last_launch_date = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=False)

    video_age = models.IntegerField(default=0)

    remove_format_webm = models.BooleanField(default=True)
    remove_format_mp4 = models.BooleanField(default=False)

    CATEGORY_HOT = 0
    CATEGORY_WEBM = 1
    CATEGORY_MP4 = 2
    CATEGORY_ADULT = 3

    VIDEO_CATEGORIES = (
        (CATEGORY_HOT, 'hot'),
        (CATEGORY_WEBM, 'webm'),
        (CATEGORY_MP4, 'mp4'),
        (CATEGORY_ADULT, 'adult'),
    )

    video_category = models.IntegerField(choices=VIDEO_CATEGORIES)

    @property
    def get_formats_to_remove_list(self):
        result = []

        if self.remove_format_webm:
            result.append('.webm')
        if self.remove_format_mp4:
            result.append('.mp4')

        return result

    @property
    def get_video_category(self):
        for pair in self.VIDEO_CATEGORIES:
            if pair[0] == self.video_category:
                return pair[1]

    def activate(self):
        if self.is_active is not True:
            self.is_active = True
            self.save()

    def deactivate(self):
        if self.is_active is True:
            self.is_active = False
            self.save()

    def update_last_launch_date(self):
        self.last_launch_date = str(timezone.now())
        self.save()